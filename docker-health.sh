#!/bin/bash

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

JSON_FILE="/srv/infrastructure/ansible/environnements.json"
LOG_FILE="/var/log/ansible-monitor.log"

echo -e "${BLUE}=== Docker Pool Health Dashboard ===${NC}"
echo ""

# 1. État des conteneurs Docker
echo -e "${GREEN}📦 Conteneurs Docker :${NC}"
TOTAL_DOCKER=$(docker ps -a --filter "name=env_" --format "{{.Names}}" | wc -l)
RUNNING=$(docker ps --filter "name=env_" --format "{{.Names}}" | wc -l)
STOPPED=$(docker ps -a -f status=exited --filter "name=env_" --format "{{.Names}}" | wc -l)
UNHEALTHY=$(docker ps --filter "name=env_" --filter "health=unhealthy" --format "{{.Names}}" | wc -l)

echo "  Total : $TOTAL_DOCKER"
echo "  Running : $RUNNING"
echo "  Stopped : $STOPPED"
echo "  Unhealthy : $UNHEALTHY"

# 2. État du JSON
echo ""
echo -e "${GREEN}📄 Fichier environnements.json :${NC}"
if [ -f "$JSON_FILE" ]; then
    TOTAL_JSON=$(jq '. | length' "$JSON_FILE" 2>/dev/null || echo "0")
    WITH_OWNER=$(jq '[.[] | select(.owner != null)] | length' "$JSON_FILE" 2>/dev/null || echo "0")
    FREE=$(jq '[.[] | select(.owner == null)] | length' "$JSON_FILE" 2>/dev/null || echo "0")
    
    echo "  Total : $TOTAL_JSON"
    echo "  Assignés : $WITH_OWNER"
    echo "  Libres : $FREE"
else
    echo -e "  ${RED}❌ Fichier non trouvé${NC}"
fi

# 3. Incohérences
echo ""
echo -e "${YELLOW}⚠️  Incohérences détectées :${NC}"

# Conteneurs dans Docker mais pas dans JSON
DOCKER_NAMES=$(docker ps -a --filter "name=env_" --format "{{.Names}}" | sort)
JSON_NAMES=$(jq -r '.[].name' "$JSON_FILE" 2>/dev/null | sort)

ORPHANS=$(comm -23 <(echo "$DOCKER_NAMES") <(echo "$JSON_NAMES"))
if [ -n "$ORPHANS" ]; then
    echo -e "  ${RED}🔴 Conteneurs orphelins (dans Docker, pas dans JSON) :${NC}"
    echo "$ORPHANS" | sed 's/^/    - /'
else
    echo -e "  ${GREEN}✅ Pas de conteneurs orphelins${NC}"
fi

# Conteneurs dans JSON mais pas dans Docker
GHOSTS=$(comm -13 <(echo "$DOCKER_NAMES") <(echo "$JSON_NAMES"))
if [ -n "$GHOSTS" ]; then
    echo -e "  ${RED}🔴 Conteneurs fantômes (dans JSON, pas dans Docker) :${NC}"
    echo "$GHOSTS" | sed 's/^/    - /'
else
    echo -e "  ${GREEN}✅ Pas de conteneurs fantômes${NC}"
fi

# 4. Liste des assignations
echo ""
echo -e "${GREEN}👥 Assignations actives :${NC}"
ASSIGNMENTS=$(jq -r '.[] | select(.owner != null) | "  \(.name) → \(.owner) (port \(.ssh_port))"' "$JSON_FILE" 2>/dev/null)
if [ -n "$ASSIGNMENTS" ]; then
    echo "$ASSIGNMENTS"
else
    echo "  Aucune assignation"
fi

# 5. Dernière exécution du monitoring
echo ""
echo -e "${GREEN}🕐 Dernière exécution du monitoring :${NC}"
if [ -f "$LOG_FILE" ]; then
    tail -3 "$LOG_FILE" | sed 's/^/  /'
else
    echo -e "  ${RED}❌ Pas de logs${NC}"
fi

# 6. Conteneurs avec problèmes SSH
echo ""
echo -e "${GREEN}🔍 Vérification SSH rapide :${NC}"
for container in $(docker ps --filter "name=env_" --format "{{.Names}}"); do
    if docker exec "$container" pgrep -x sshd >/dev/null 2>&1; then
        echo -e "  ${GREEN}${NC} $container : SSH OK"
    else
        echo -e "  ${RED}${NC} $container : SSH DOWN"
    fi
done

# 7. Résumé
echo ""
echo -e "${BLUE}=== Résumé ===${NC}"
if [ "$TOTAL_DOCKER" -eq "$TOTAL_JSON" ] && [ -z "$ORPHANS" ] && [ -z "$GHOSTS" ] && [ "$UNHEALTHY" -eq 0 ]; then
    echo -e "${GREEN} Tout est OK !${NC}"
else
    echo -e "${YELLOW}  Des problèmes ont été détectés${NC}"
    [ -n "$ORPHANS" ] && echo -e "  ${RED}→ Exécuter le playbook pour synchroniser${NC}"
fi