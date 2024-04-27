import math;

from enum import Enum, auto;

class ColorScheme(Enum):
  GREEN_RED  = auto();
  RED_YELLOW = auto();
  WIKIPEDIA  = auto();
  CUSTOM     = auto();

ColorSchemes = [
    ColorScheme.GREEN_RED,
    ColorScheme.RED_YELLOW,
    ColorScheme.WIKIPEDIA,
    ColorScheme.CUSTOM
];

################################################################################

class Interpolation(Enum):
  LINEAR = auto();
  COSINE = auto();

def Interpolate(a : float, b : float, t : float, type_ = Interpolation.LINEAR) -> float:
  if type_ == Interpolation.LINEAR:
    return (1.0 - t) * a + t * b;
  else:
    return ( math.cos(t * math.pi) + 1 ) * 0.5 * (a - b) + b;

################################################################################

def Dot(v1 : tuple, v2 : tuple) -> float:
  return v1[0] * v2[0] + v1[1] * v2[1];

################################################################################

def VectorFromAngle(angle : float) -> tuple:
  x = math.cos(angle * 0.017453292519943295);
  y = math.sin(angle * 0.017453292519943295);

  return (x, y);

################################################################################

def NoiseToColor(noiseVal : float, colorScheme : ColorScheme) -> tuple:
  if noiseVal < 0.0:
    val = int(noiseVal);
    clr = -255 if val < -255 else val;
    if colorScheme == ColorScheme.GREEN_RED:
      return (255.0, 255.0 + clr, 0.0);
    elif colorScheme == ColorScheme.RED_YELLOW:
      return (255.0 + clr, 0.0, 0.0);
    elif colorScheme == ColorScheme.CUSTOM:
      return (0.0, 255.0 + clr, 255.0 + clr);
    else:
      return (255.0 + clr, 255.0, 255.0 + clr);
  else:
    val = int(noiseVal);
    clr = 255 if val > 255 else val;
    if colorScheme == ColorScheme.GREEN_RED:
      return (255.0 - clr, 255.0, 0.0);
    elif colorScheme == ColorScheme.RED_YELLOW:
      return (255.0, clr, 0.0);
    elif colorScheme == ColorScheme.CUSTOM:
      return (0.0, 255.0 - clr, 255.0 - clr);
    else:
      return (255.0, 255.0 - clr, 255.0);
