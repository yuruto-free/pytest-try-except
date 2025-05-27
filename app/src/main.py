from .newton import Newton1d

def calc_square(x, target=2):
  return (x - target) ** 2

def main():
  instance = Newton1d(calc_square)
  target = 3
  x0 = target + 1
  hat_x = instance.estimate(x0, target=target)
  histories = instance.histories

  # Ouput estimated value
  print(f'Estimated value: {hat_x}')
  # Show history
  for store in histories:
    idx, val = store.get_pair()
    print(f'{idx:05d}: {val}')

if __name__ == '__main__':
  main()