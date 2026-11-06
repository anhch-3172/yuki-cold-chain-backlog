#!/usr/bin/env bash
# Agent ghi SWP + giờ lên GitHub Project (v2) bằng gh CLI.
# Cách dùng: bash push_to_project.sh out/swp.tsv <owner> <project-number>
# Yêu cầu: gh auth status OK (scope project), jq; Project có field Number "SWP", "Giờ ước lượng"
#          và Single select "SWP reviewed" (Yes/No). Issue có tiêu đề bắt đầu bằng "[<id>]".
set -euo pipefail
TSV="$1"; OWNER="$2"; NUM="$3"
PID=$(gh project view "$NUM" --owner "$OWNER" --format json | jq -r .id)
FIELDS=$(gh project field-list "$NUM" --owner "$OWNER" --format json --limit 50)
fid(){ echo "$FIELDS" | jq -r --arg n "$1" '.fields[] | select(.name==$n) | .id'; }
F_SWP=$(fid "SWP"); F_H=$(fid "Giờ ước lượng"); F_R=$(fid "SWP reviewed")
OPT_YES=$(echo "$FIELDS" | jq -r '.fields[] | select(.name=="SWP reviewed") | .options[] | select(.name=="Yes") | .id')
ITEMS=$(gh project item-list "$NUM" --owner "$OWNER" --format json --limit 500)
tail -n +2 "$TSV" | while IFS=$'\t' read -r id final hours; do
  item=$(echo "$ITEMS" | jq -r --arg p "[$id]" '.items[] | select(((.content.title // .title) // "")|startswith($p)) | .id' | head -1)
  if [ -z "$item" ]; then echo "SKIP $id (không thấy issue)"; continue; fi
  gh project item-edit --project-id "$PID" --id "$item" --field-id "$F_SWP" --number "$final" >/dev/null
  gh project item-edit --project-id "$PID" --id "$item" --field-id "$F_H" --number "$hours" >/dev/null
  gh project item-edit --project-id "$PID" --id "$item" --field-id "$F_R" --single-select-option-id "$OPT_YES" >/dev/null
  echo "OK $id SWP=$final giờ=$hours"
done
