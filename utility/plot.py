import matplotlib.pyplot as plt
import numpy as np

# filepath = "../data/acquisition(1)/data.txt"


def plot_orientation(filepath):
    try:
        data = np.loadtxt(filepath, usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))
    except:
        lines = open(filepath).readlines()
        open(filepath, 'w').writelines(lines[:-1])
        data = np.loadtxt(filepath,usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))

    plt.figure(1)

    plt.subplot(211)
    plt.title('orientation quaternion')
    plt.plot(data[:,1], data[:,5], 'r', data[:,1], data[:,6], 'g', data[:,1], data[:,7], 'b', data[:,1], data[:,8], 'y')

    plt.subplot(212)
    plt.title('orientation euler')
    plt.plot(data[:,1], data[:,2], 'r', data[:,1], data[:,3], 'g', data[:,1], data[:,4], 'b')


    plt.figure(2)

    plt.subplot(211)
    plt.title('shoulder orientation quaternion')
    plt.plot(data[:,1], data[:,12], 'r', data[:,1], data[:,13], 'g', data[:,1], data[:,14], 'b', data[:,1], data[:,15], 'y')

    plt.subplot(212)
    plt.title('shoulder orientation euler')
    plt.plot(data[:,1], data[:,9], 'r', data[:,1], data[:,10], 'g', data[:,1], data[:,11], 'b')



    plt.show()

if __name__ == "__main__":
    filepath = "../data/acquisition(1)/data.txt"
    plot_orientation(filepath)


