import math;
import random;

from enum import Enum, auto;

################################################################################

class Interpolation(Enum):
  LINEAR = auto()
  COSINE = auto()

################################################################################

class Noise2D:
  _rnd     = [];
  _noise   = [];
  _size    = 0;
  _seed    = None;
  _octaves = 8;
  _interpolation = Interpolation.LINEAR;
  _scalingBias = 1.0;

  # ----------------------------------------------------------------------------

  def __init__(self,
               size : int,
               octaves=8,
               seed=None,
               interpolation=Interpolation.LINEAR,
               scalingBias=1.0):
    self._seed    = seed;
    self._size    = size;
    self._octaves = octaves;

    self._interpolation = interpolation;

    self._scalingBias = scalingBias;

    if self._scalingBias < 0.1:
      self._scalingBias = 0.1;

    random.seed(self._seed);

    self.Reset();

  # ----------------------------------------------------------------------------

  def Reset(self):
    self._rnd   = [ [ 0.0 for _ in range(self._size) ] for _ in range(self._size) ];
    self._noise = [ [ 0.0 for _ in range(self._size) ] for _ in range(self._size) ];

    #
    # Generate seed array.
    #
    for x in range(self._size):
      for y in range(self._size):
        self._rnd[x][y] = random.random();

    for x in range(self._size):
      for y in range(self._size):

        noise = 0.0;
        scale = 1.0;
        normCoeff = 0;

        for o in range(1, self._octaves):
          pitch = (self._size >> o);

          if pitch == 0:
            break;

          indx1 = (x // pitch) * pitch;
          indy1 = (y // pitch) * pitch;

          indx2 = (indx1 + pitch) % self._size;
          indy2 = (indy1 + pitch) % self._size;

          blendX = float(x - indx1) / float(pitch);
          blendY = float(y - indy1) / float(pitch);

          if self._interpolation == Interpolation.LINEAR:
            sampleX = (1.0 - blendX) * self._rnd[indx1][indy1] + blendX * self._rnd[indx2][indy1];
            sampleY = (1.0 - blendX) * self._rnd[indx1][indy2] + blendX * self._rnd[indx2][indy2];
          else:
            sampleX = (math.cos(blendX * math.pi) + 1) * 0.5 * (self._rnd[indx1][indy1] - self._rnd[indx2][indy1]) + self._rnd[indx2][indy1];
            sampleY = (math.cos(blendX * math.pi) + 1) * 0.5 * (self._rnd[indx1][indy2] - self._rnd[indx2][indy2]) + self._rnd[indx2][indy2];

          noise += (blendY * (sampleY - sampleX) + sampleX) * scale;
          normCoeff += scale;
          scale /= (2.0 * self._scalingBias);

        #
        # Rescale result back to [ 0.0 ; 1.0 ]
        #
        if normCoeff != 0:
          self._noise[x][y] = noise / normCoeff;

  # ----------------------------------------------------------------------------

  def Noise(self, x : float, y : float) -> float:
    xx = int(x) % self._size;
    yy = int(y) % self._size;

    return self._noise[xx][yy];
