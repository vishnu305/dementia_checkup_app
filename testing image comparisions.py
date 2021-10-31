from skimage.metrics import structural_similarity
import cv2


def structural_sim(img1,img2):
    sim, diff = structural_similarity(img1,img2,full=True)
    return sim

def orb_sim(img1,img2):
    orb = cv2.ORB_create()
    kp_a, desc_a = orb.detectAndCompute(img1,None)
    kp_b, desc_b = orb.detectAndCompute(img2,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
    matches = bf.match(desc_a,desc_b)
    similarity_regions = [i for i in matches if i.distance<50]
    if len(matches) == 0:
        return 0
    return len(similarity_regions)/len(matches)

image1 = cv2.imread('Image.jpg',0)
image2 = cv2.imread('user_input.jpg',0)

# print('structural similarity',structural_sim(image1,image2))

print('orbital similarity',orb_sim(image1,image2))