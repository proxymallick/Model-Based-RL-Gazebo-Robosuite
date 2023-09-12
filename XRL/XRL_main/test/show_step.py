import math
import sys

class view_bar:
    def __init__(self, message, num, total, value_name, value_data):
        self.message = message
        self.num = num
        self.total = total
        rate = self.num  / self.total
        rate_num = int(rate * 40)
        rate_nums = math.ceil(rate * 100)
        r = '\r%s:[%s%s]%d%%\t%d/%d\t%s%f' % (self.message, "=" * rate_num,
                                        " " * (40 - rate_num), rate_nums, self.num , self.total, value_name, value_data)

        sys.stdout.write(r)
        sys.stdout.flush()

# a =10
# for i in range(60000):
#     view_bar("epoch ", i+1, 60000, 'a = ', float(a))
#     a += 0.01
