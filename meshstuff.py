import numpy as np

# Mesh class

# initial_state should be an array. Dimentions of initial_state
# when mesh is created determine dimentions of mesh

# stencil is a list of lists of index offsets that determines 
# which nodes are considered neighbors

class Mesh:
    def __init__(self, initial_state, stencil, **kwargs):
        self.state = np.array(initial_state)
        self.stencil = stencil
        self.fixed = None
        self.history = []
        self.diffusivity = 1
        self.nd_spacing = 1


    # neighbors method returns tuple giving indices and values of nodes neighboring input_node
    def neighbors(self, input_node):
        s = self.state
        # use stencil to find neighbors
        all_nb = []
        for offset in self.stencil:
            all_nb.append([this_i + diff for this_i, diff in zip(tuple(input_node), offset)])

        # TODO: rewrite this part to account for different boundary condition types
        values = []
        for idx in all_nb:
            try:
                values.append(s[tuple(idx)])
            except:
                values.append(0)
        return all_nb, values

    # print() wasn't very readable
    def niceprint(self):
        print('')
        try:
            for r in self.state:
                for c in r:
                    n = str(round(c, 2))
                    n = n.zfill(4)
                    n = n.rjust(7, ' ')
                    print(n, end='')
                print('')
        except:
            for r in self.state:
                n = str(round(r,2))
                n = n.rjust(7, ' ')
                print(n, end='')
        print('')



    # finds next num_steps states of mesh
    # stores past states in self.history
    def explicit_sim(self, update_fn, num_steps, stepsize, **kwargs):
        msginterval = int(num_steps/10)
        print("simulating", num_steps, "timesteps")
        if self.fixed is not None:
            fixedvals = []
            for i in self.fixed:
                fixedvals.append(self.state[i])
        else:
            fixedvals = None
        for s in range(num_steps):
            if s >= msginterval:
                print("current step:",s)
                msginterval += int(num_steps/10)

            nextstate = np.zeros(np.shape(self.state))
            with np.nditer(self.state, flags=['multi_index']) as it:
                for x in it:
                    nextstate[it.multi_index] = update_fn(self, it.multi_index, stepsize)
            if fixedvals is not None:
                for i in range(len(self.fixed)):
                    nextstate[self.fixed[i]] = fixedvals[i]
            self.state = np.copy(nextstate)
            self.history.append(self.state)
            if kwargs:
                if kwargs['debug'] == 1:
                    self.niceprint()
                    input("")
        print("")

    def implicit_sim(self, update_fn, num_steps, stepsize, **kwargs):
        msginterval = int(num_steps/10)
        if self.fixed is not None:
            fixedvals = []
            for i in self.fixed:
                fixedvals.append(self.state[i])
        else:
            fixedvals = None
        for s in range(num_steps):
            if s >= msginterval:
                print("current step:", s)
                msginterval += int(num_steps/10)
            self.history.append(self.state)
            self.state = update_fn(self, stepsize)
            if fixedvals is not None:
                for i in range(len(self.fixed)):
                    self.state[self.fixed[i]] = fixedvals[i]
            if kwargs:
                if kwargs['debug'] == 1:
                    self.niceprint()
                    input("")
        print("")
            








    



