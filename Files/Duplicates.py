class Solution:
    def Duplicates(self, nums):
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False

print(Solution().Duplicates([1, 4, 3, 2]))