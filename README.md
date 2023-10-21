# Athena
Athena is a framework for organizing code execution across a distributed cluster.  Specifically, it handles typed object serialization akin to [Protocol Buffers](https://github.com/protocolbuffers/protobuf) in a terse and Pythonic manner, as well as utilizing its embedded structure to auto-generate method validation unit tests.

## Getting Started

Create a scratch file that represents an example piece of distributed computation:

```
from athena.exec import run
from athena.state import State
from athena.environment import Environment
from athena.helpers.structure import structure
from athena.helpers.validate import validate


class MyEnvironment(Environment):
    @structure
    class Var:
        SEED: int = 1

class MyState(State):
    env: MyEnvironment
    @structure
    class Data:
        test: int = 2

class MyModel:
    @staticmethod
    @validate
    def main(state: MyState):
        state.Data.test = state.Data.test + state.env.Var.SEED
        return state

run(MyModel)
```

Running the model displays the result, note that since the test variable and seed constant default to a sum of 3:
```
> python compute.py
[athena.exec:20] {'test': 3}
```

We can mock a non-default value for the input state by creating a `message.json` in the base directory:
```
{"test":  1}
```

```
> python compute.py
[athena.exec:20] {'test': 2}
```

Any modifications to our environment will be reflected in our Python environment:

```
> export SEED=3
> python compute.py
[athena.exec:20] {'test': 4}
```

Note that unit tests for our method are automatically generated in the `/tests/` subdirectory.  These files can be optionally be checked in and set to auto-run via a pull request builder via `athena.test` to ensure the consistency of methods are maintained over time.

Note the defined limitations in the framework: `structure` must decorate an inner class of a `State` or `Environment` object, and `validate` must decorate a static method that receives and returns a state.

## Patron

<a href="https://en.wikipedia.org/wiki/Pallas_Athena_(Rembrandt)"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Pallas_Athena_or%2C_Armoured_Figure_by_Rembrandt_Harmensz._van_Rijn.jpg/599px-Pallas_Athena_or%2C_Armoured_Figure_by_Rembrandt_Harmensz._van_Rijn.jpg" alt="Pallas Athena" width="300" height="400"></a>
