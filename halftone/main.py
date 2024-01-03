from PIL import Image
import numpy as np

def apply_kernel(img, f, side=5):
    # TODO: Better type definition of f
    '''Apply a square kernel f to the image 

    f is the sidexside kernel from the image as input and returns a sidexside kernel as output.
    '''

    print(img.shape)
    rpad = side - (img.shape[0] % side)
    cpad = side - (img.shape[1] % side)

    rows = img.shape[0] + rpad
    cols = img.shape[1] + cpad

    arr = np.zeros(img.shape)
    arr = np.pad(arr, ((0,rpad), (0,cpad)), constant_values=0)

    img = np.pad(img, ((0,rpad), (0,cpad)), constant_values=0)

    print(img.shape)

    for row in range(0,rows,side):
        for col in range(0,cols,side):
            arr[row:row+side,col:col+side] = f(img[row:row+side,col:col+side])

    return arr[0:rows-rpad, 0:cols-cpad]

if __name__ == '__main__':
    img = Image.open('lenna.png')
    gimg = img.convert('L')

    # First: given an image, pad it such that it's a multiple of 5.

    arr = np.array(gimg)
    # Pad width and height separately.
    #arr = np.pad(arr, (arr.shape[0] % 5, arr.shape[1] % 5), constant_values=0)
    #print(arr.shape)


    # Given an image, modify a square slice of it 

    #arr[0:5,0:5] = 0
    def avg_kernel(img: np.ndarray, invert=False):
        #print(img.shape)

        i = 255 if invert else 0

        k0 = np.abs(np.array([
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ])*255 - i)

        k1 = np.abs(np.array([
            [0,0,0,0,0],
            [0,0,1,0,0],
            [0,1,0,1,0],
            [0,0,1,0,0],
            [0,0,0,0,0]
        ])*255 - i)

        k2 = np.abs(np.array([
            [0,0,0,0,0],
            [0,1,0,1,0],
            [0,0,1,0,0],
            [0,1,0,1,0],
            [0,0,0,0,0]
        ])*255 - i)

        k3 = np.abs(np.array([
            [0,0,0,0,0],
            [0,1,1,1,0],
            [0,1,0,1,0],
            [0,1,1,1,0],
            [0,0,0,0,0]
        ])*255 - i)

        mapping = [ k0, k1, k2, k3 ]

        region = 256/4
        mean = int(img.mean())

        #print(mapping[int(mean/region)])

        return mapping[int(mean/region)]
        '''
        k = np.ones(img.shape)*mean

        return k
        '''

        return

    arr = apply_kernel(arr, lambda k: avg_kernel(k, invert=False), side=5)
    print(f'Final shape: {arr.shape}')
    print(arr)

    halftone_img = Image.fromarray(arr).convert('L')
    halftone_img.save('halftone.png')
    halftone_img.show()
    '''
    print(arr.shape[0] % 5)
    # Here is a 5x5 kernel slice from the image
    print(arr[0:5,0:5])
    '''