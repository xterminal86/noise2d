import argparse;
import pygame;

from noise2d import Noise2D, Interpolation;

################################################################################

def main():
  parser = argparse.ArgumentParser();

  parser.add_argument("SIZE",   type=int, help="E.g. 512");
  parser.add_argument("--seed", type=int, default=1, help="E.g. 1234. Default: 1");

  args = parser.parse_args();

  seed = 1;
  size = args.SIZE;

  screenSize = [ 1280, 720 ];

  pygame.init();

  pygame.display.set_caption("noise2d demo");

  screen = pygame.display.set_mode(screenSize);

  running = True;

  clock = pygame.time.Clock();

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

################################################################################

if __name__ == "__main__":
  main();
