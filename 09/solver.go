package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Return the pairwise difference of elements in a slice.
func pairwiseDifference(nums []int) []int {
	var diffs []int
	for i := 0; i < len(nums)-1; i++ {
		diffs = append(diffs, nums[i+1]-nums[i])
	}
	return diffs
}

// Check if all elements in the slice are zeros.
func allZeros(nums []int) bool {
	for _, num := range nums {
		if num != 0 {
			return false
		}
	}
	return true
}

func solveFirst(lines []string) int {
	total := 0
	for _, line := range lines {
		parts := strings.Fields(line)
		numbers := make([]int, len(parts))
		for i, part := range parts {
			numbers[i], _ = strconv.Atoi(part)
		}

		allDifferences := [][]int{numbers}
		differences := pairwiseDifference(numbers)
		for !allZeros(differences) {
			allDifferences = append(allDifferences, differences)
			differences = pairwiseDifference(differences)
		}

		for i := len(allDifferences) - 2; i >= 0; i-- {
			last := allDifferences[i][len(allDifferences[i])-1]
			nextLast := allDifferences[i+1][len(allDifferences[i+1])-1]
			allDifferences[i] = append(allDifferences[i], last+nextLast)
		}

		res := allDifferences[0][len(allDifferences[0])-1]
		total += res
	}
	return total
}

func solveSecond(lines []string) int {
	total := 0
	for _, line := range lines {
		parts := strings.Fields(line)
		numbers := make([]int, len(parts))
		for i, part := range parts {
			numbers[i], _ = strconv.Atoi(part)
		}

		allDifferences := [][]int{numbers}
		differences := pairwiseDifference(numbers)
		for !allZeros(differences) {
			allDifferences = append(allDifferences, differences)
			differences = pairwiseDifference(differences)
		}

		for i := len(allDifferences) - 2; i >= 0; i-- {
			first := allDifferences[i][0]
			nextFirst := allDifferences[i+1][0]
			allDifferences[i] = append([]int{first - nextFirst}, allDifferences[i]...)
		}

		res := allDifferences[0][0]
		total += res
	}
	return total
}

func solve(filepath string) {
	file, err := os.Open(filepath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	fmt.Println("A:", solveFirst(lines))
	fmt.Println("B:", solveSecond(lines))
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Please provide a file path")
		return
	}
	solve(os.Args[1])
}
