import math

# Dataset
data = [1,2,3,8,9,10]

# Initial parameters
mean1 = 2
mean2 = 9

var1 = 1
var2 = 1

weight1 = 0.5
weight2 = 0.5

# Gaussian function
def gaussian(x, mean, var):
    return (1/math.sqrt(2*math.pi*var)) * math.exp(-(x-mean)**2/(2*var))

# Run EM for few iterations
for iteration in range(5):

    print("Iteration:", iteration+1)

    # Expectation step
    responsibilities = []

    for x in data:
        p1 = weight1 * gaussian(x,mean1,var1)
        p2 = weight2 * gaussian(x,mean2,var2)

        r1 = p1/(p1+p2)
        r2 = p2/(p1+p2)

        responsibilities.append((r1,r2))

    # Maximization step
    sum_r1 = sum(r[0] for r in responsibilities)
    sum_r2 = sum(r[1] for r in responsibilities)

    mean1 = sum(responsibilities[i][0]*data[i] for i in range(len(data)))/sum_r1
    mean2 = sum(responsibilities[i][1]*data[i] for i in range(len(data)))/sum_r2

    weight1 = sum_r1/len(data)
    weight2 = sum_r2/len(data)

    print("Mean1:",mean1," Mean2:",mean2)
