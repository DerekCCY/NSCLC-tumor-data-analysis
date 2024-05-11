class Sort:
    def merge(self, left, right):
        ''' 兩數列合併 '''
        output = []
        while left and right:
            if left[0] >= right[0]:
                output.append(left.pop(0))
            else:
                output.append(right.pop(0))
        if left:
            output += left
        if right:
            output += right
        return output
    def merge_sort(self, nlst):
        ''' 合併排序 '''
        if len(nlst) <= 1:
            return nlst
        mid = len(nlst) // 2
        left = nlst[:mid]
        right = nlst[mid:]
        left = self.merge_sort(left)
        right = self.merge_sort(right)
        return self.merge(left, right)