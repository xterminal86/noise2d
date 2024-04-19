import argparse;
import random

import pygame;

# from noise2d import Noise2D, Interpolation;
from noise2d_new import NewNoise2D;

################################################################################

class ProgramData:
  _shouldStop = False;
  _seed       = 1;
  _resolution = 16;
  _step       = 1;
  _screenSize = tuple();
  _noiseObj   = None;

################################################################################

def ProcessEvents(pd : ProgramData):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pd._shouldStop = True;
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pd._shouldStop = True;
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        pd._noiseObj.Noise(event.pos[0], event.pos[1]);

################################################################################

def Draw(screen, pd : ProgramData):
  screen.fill( (0, 0, 0) );

  gridColor    = pygame.Color("#AA00AA");
  gradVecColor = pygame.Color("#00AA00");

  gradLen = pd._step // 2;

  for x in range(0, pd._screenSize[0], pd._step):
    pygame.draw.line(screen, gridColor, (x, 0), (x, pd._screenSize[1]));
    pygame.draw.line(screen, gridColor, (0, x), (pd._screenSize[0], x));

  for x in range(pd._resolution):
    for y in range(pd._resolution):
      gradVec = pd._noiseObj._gradients[x][y];
      gradVec = (gradVec[0] * gradLen, gradVec[1] * gradLen);

      cornerCoords = (y * pd._step, x * pd._step);
      vecEnd  = (cornerCoords[0] + gradVec[0], cornerCoords[1] + gradVec[1]);
      pygame.draw.line(screen, gradVecColor, cornerCoords, vecEnd);
      pygame.draw.circle(screen, gradVecColor, vecEnd, 2);

  pygame.display.flip();

################################################################################

def main():
  parser = argparse.ArgumentParser();

  parser.add_argument("RESOLUTION",
                      type=int,
                      help="Noise grid resolution. E.g. 32");
  parser.add_argument("--seed",
                      type=int,
                      default=None,
                      help="RNG seed. E.g. 1234. Default: None");

  args = parser.parse_args();

  screenSize = ( 1280, 720 );

  pygame.init();

  pygame.display.set_caption("noise2d demo");

  screen = pygame.display.set_mode(screenSize);

  pd = ProgramData();
  pd._resolution = args.RESOLUTION;

  if pd._resolution < 1:
    pd._resolution = 1;

  if pd._resolution > screenSize[1]:
    pd._resolution = screenSize[1];

  pd._seed       = args.seed;
  pd._screenSize = screenSize;
  pd._step       = pd._screenSize[0] // pd._resolution;

  print(f"STEP = { pd._step }");

  random.seed(pd._seed);

  clock = pygame.time.Clock();

  pd._noiseObj = NewNoise2D(pd._resolution, pd._step);

  while not pd._shouldStop:

    clock.tick(60);

    ProcessEvents(pd);
    Draw(screen, pd);

  pygame.quit();

  '''
  bias = 1.0;
  intpl = Interpolation.LINEAR;
  noise = Noise2D(size, seed=seed, interpolation=intpl, scalingBias=bias);

  while running:

    clock.tick(60);

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False;
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          running = False;
        elif event.key == pygame.K_i:
          if intpl == Interpolation.LINEAR:
            intpl = Interpolation.COSINE;
          else:
            intpl = Interpolation.LINEAR;

          print(intpl);

          noise = Noise2D(size, seed=seed, interpolation=intpl, scalingBias=bias);
        elif event.key == pygame.K_z:
          bias -= 0.1;

          if bias < 0.1:
            bias = 0.1;

          print(f"bias = { bias }");

          noise = Noise2D(size, seed=seed, interpolation=intpl, scalingBias=bias);

        elif event.key == pygame.K_x:
          bias += 0.1;

          if bias > 2.0:
            bias = 2.0;

          print(f"bias = { bias }");

          noise = Noise2D(size, seed=seed, interpolation=intpl, scalingBias=bias);

    screen.fill((0,0,0));

    for x in range(screenSize[0]):
      for y in range(screenSize[1]):
        c = int(noise.Noise(x, y) * 255);
        if c > 255:
          c = 255;

        clr = (c, c, c);

        pygame.draw.circle(screen,
                           clr,
                           (x, y),
                           1);

    pygame.display.flip();

  pygame.quit();
  '''

################################################################################

if __name__ == "__main__":
  main();
