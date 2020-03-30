jq '.Keys | keys | .[]' new-pins.json -r | tee /dev/stderr | xargs -n 1 ipfs pin add --recursive
