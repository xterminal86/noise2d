import math;

from enum  import Enum, auto;

################################################################################

class TextAlign(Enum):
  LEFT   = auto();
  RIGHT  = auto();
  CENTER = auto();

def PrintString(screen,
                font,
                text,
                pos : tuple,
                color : tuple,
                align : TextAlign = TextAlign.LEFT):
  ts, s = font.render(text, color);
  p = pos;
  if align == TextAlign.RIGHT:
    p = (pos[0] + s[2], pos[1]);
  elif align == TextAlign.CENTER:
    p = (pos[0] - s[2] // 2, pos[1]);
  screen.blit(ts, p);

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

def NoiseToColor(noiseVal : float) -> tuple:
  if noiseVal < 0.0:
    val = int(abs(noiseVal));
    clr = 255 if val > 255 else val;
    return (clr, 0, 0);
  else:
    val = int(noiseVal);
    clr = 255 if val > 255 else val;
    return (clr, clr, 0);
