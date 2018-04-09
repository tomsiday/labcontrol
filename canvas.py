## This short file lets us put matplotlib plots into the PyQt4 gui framework 
## is copy-pasted from matplotlib docs (or similar)

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas 
import matplotlib.pyplot as plt

class Canvas(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = plt.figure()
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)