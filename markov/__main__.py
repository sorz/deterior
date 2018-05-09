from .dataset import load_inspect_log
from .trainning import build_simple_model

def main():
    records, n_state = load_inspect_log('test.csv')
    model, result = build_simple_model(n_state, records)
    print(result)

if __name__ == '__main__':
    main()