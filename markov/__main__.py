from .dataset import load_inspect_log
from .trainning import build_simple_model
from .models import Model

def main():
    records, n_state = load_inspect_log('test.csv')
    model, result = build_simple_model(n_state, records)
    print(result)
    print(model.mat)
    with open('model.json', 'w') as f:
        model.dump(f)
    with open('model.json') as f:
        model = Model.load(f)
    print(model.mat)

if __name__ == '__main__':
    main()