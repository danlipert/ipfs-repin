cat delta-pins.keys | tee /dev/stderr | xargs -n 1 ipfs pin add --recursive
