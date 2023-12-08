#!/bin/bash
set -e

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "No argument provided. Please provide a number."
    exit 1
fi

# Check if the argument is a number
if ! [[ $1 =~ ^[0-9]+$ ]]; then
    echo "The provided argument is not a number."
    exit 1
fi

echo "The provided argument is a number: $1"

dir_name=$(printf "%02d" $1)

mkdir -p "$dir_name"
rm -f "${dir_name}/puzzle.md"
aoc -d "$1" d -i "${dir_name}/input.txt" -p "${dir_name}/puzzle.md"
