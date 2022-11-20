
import logging
logger = logging.getLogger(__name__)
import cv2
logger.warning("wf")
logger.warning("wf")
from fer import FER
logger.warning("wf")
import matplotlib.pyplot as plt
logger.warning("wf")
import matplotlib.image as mpimg
logger.warning("wf")

#Class that does all the machine learning processing
class EmotionalAnalyzer:

  #Initialization, which initializes the FER package
  def __init__(self):
    self.emotion_detector = FER()

  #Analyzes image and returns values of each image
  def analyzeImage(self, imgDirectory):
    self.file = imgDirectory
    logger.debug(self.file)
    self.input_image = cv2.imread(self.file)
    # Output image's information
    # Save output in result variable
    self.result = self.emotion_detector.detect_emotions(self.input_image)
    logger.debug(self.result)

    # self.createImage(saveImage=True, showImage=False)
    return self.result
  
  def createImage(self, saveImage = False, showImage = False):
    bounding_box = self.result[0]["box"]
    emotions = self.result[0]["emotions"]
    cv2.rectangle(self.input_image,(
      bounding_box[0], bounding_box[1]),(
      bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                  (0, 155, 255), 2,)

    emotion_name, score = self.emotion_detector.top_emotion(self.input_image)
    for index, (emotion_name, score) in enumerate(emotions.items()):
      color = (211, 211,211) if score < 0.01 else (255, 0, 0)
      emotion_score = "{}: {}".format(emotion_name, "{:.2f}".format(score))
    
      cv2.putText(self.input_image,emotion_score,
                  (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + index * 15),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,color,1,cv2.LINE_AA,)
    
    #Save the result in new image file
    if (saveImage):    
      cv2.imwrite(self.file.replace(".", "_out."), self.input_image)

    # Read image file using matplotlib's image module
    if (showImage):
      result_image = mpimg.imread(self.file.replace(".", "_out."))
      # Display Output Image
      plt.show()

if __name__ == "__main__":
	analyzer = EmotionalAnalyzer()