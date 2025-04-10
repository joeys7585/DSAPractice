class Solution:
    def productExceptSelf(self, nums):
        n = len(nums)
        ans =[1]*n

        left = 1
        right = 1
        for i in range(n):
            ans[i] = left
            left *= nums[i]
        for i in range(n-1, -1, -1):
            ans[i] *= right
            right *= nums[i]
        return ans
print(Solution().productExceptSelf([1,2,3,4,5, 2, 1]))