import copy
#%%
widen_h = 10
#%%
class intervalES:
    def __init__(self, l = 0, h = 0, type = 0):
        # self.type -1 bottom, 1 top, 0 normal
        if l>=widen_h and h>=widen_h:
            self.type = 1
            self.l = widen_h
            self.h = widen_h
        elif h>=widen_h:
            self.type = 0
            self.l = l
            self.h = widen_h
        else:
            self.type = type
            self.l = l
            self.h = h

    def join(self, secondItvES):
        if self.type == -1 and secondItvES.type == -1:
            return intervalES(type=-1)
        elif self.type == -1:
            return intervalES(secondItvES.l, secondItvES.h, secondItvES.type)
        elif secondItvES.type == -1:
            return intervalES(self.l, self.h, self.type)
        else:
            return intervalES(min(self.l, secondItvES.l), max(self.h, secondItvES.h))

    def update(self, l, h):
        if l>=widen_h and h>=widen_h:
            self.type = 1
            self.l = widen_h
            self.h = widen_h
        elif h>=widen_h:
            self.type = 0
            self.l = l
            self.h = widen_h
        else:
            self.type = 0
            self.l = l
            self.h = h

    def diff(self, secondItvES):
        return self.type == secondItvES.type and \
               self.l == secondItvES.l and \
               self.h == secondItvES.h

    def __str__(self):
        if self.type == -1:
            return "bottom"
        elif self.type == 1:
            return "top"
        else:
            return "[{}, {}]".format(self.l, self.h)
#%%
class abstractState:
    def __init__(self):
        self.state = [intervalES(type=-1) for i in range(3)]

    def join(self, secondAbstractState):
        res = abstractState()
        for i in range(len(self.state)):
            res.state[i] = self.state[i].join(secondAbstractState.state[i])
        assert isinstance(res, abstractState)
        return res

    def diff(self, secondAbstractState):
        res = True
        for i in range(len(self.state)):
            if not self.state[i].diff(secondAbstractState.state[i]):
                res = False
        return res

    def __str__(self):
        return "[i->{}, j->{}, x->{}]".format(str(self.state[0]), str(self.state[1]), str(self.state[2]))
#%%
def join_multiple_as(as_list):
    assert len(as_list) > 0
    res = copy.deepcopy(as_list[0])
    for abstract_state in as_list[1:]:
        res = res.join(abstract_state)
    return res
#%%
def fs_0(present_states, next_states):
    return False

def fs_1(present_states, next_states):
    InES = join_multiple_as((present_states[0], ))
    next_states[1] = InES
    next_states[1].state[0].update(0, 0)
    return next_states[1].diff(present_states[1])

def fs_2(present_states, next_states):
    InES = join_multiple_as((present_states[1], present_states[5]))
    next_states[2] = InES
    assert isinstance(InES, abstractState)
    next_states[2].state[1].update(InES.state[0].l, InES.state[0].h, InES.state[0].type)
    return next_states[2].diff(present_states[2])

def fs_3(present_states, next_states):
    InES = join_multiple_as((present_states[2], present_states[4]))
    next_states[3] = InES
    next_states[3].state[2].update(InES.state[0].l * InES.state[0].l, InES.state[0].h * InES.state[0].h, InES.state[0].type)
    return next_states[3].diff(present_states[3])

def fs_4(present_states, next_states):
    InES = join_multiple_as((present_states[3], ))
    next_states[4] = InES
    next_states[4].state[1].update(InES.state[1].l+1, InES.state[1].h+1, InES.state[1].type)
    return next_states[4].diff(present_states[4])

def fs_5(present_states, next_states):
    InES = join_multiple_as((present_states[4], ))
    next_states[5] = InES
    next_states[5].state[0].update(InES.state[0].l+1, InES.state[0].h+1, InES.state[0].type)
    return next_states[5].diff(present_states[5])
#%%
def get_successor(i):
    assert i>=0 and i <=5
    successor_dict = {
        0: [1],
        1: [2],
        2: [3],
        3: [4],
        4: [3, 5],
        5: [2]
    }
    return successor_dict[i]
#%%
init_states = [abstractState() for i in range(6)]
#%%
# worklist algorithm

present_states = copy.deepcopy(init_states)
print("=========round {}==========".format(0))
for i in range(len(present_states)):
    print("node {}: {}".format(i, str(present_states[i])))
print("\n\n")

run_flg = True
worklist = {0, 1, 2, 3, 4, 5}
next_worklist = set()
transfer_funcs = [fs_0, fs_1, fs_2, fs_3, fs_4, fs_5]
round_counter = 1
while run_flg:
    next_states = copy.deepcopy(present_states)
    for i in worklist:
        same_flg = transfer_funcs[i](present_states, next_states)
        if not same_flg:
            next_worklist = next_worklist.union(set(get_successor(i)))
    present_states = copy.deepcopy(next_states)
    print("=========round {}==========".format(round_counter))
    for i in range(len(present_states)):
        print("node {}: {}".format(i, str(present_states[i])))
    print("\n\n")

    if len(next_worklist) == 0:
        run_flg = False
    worklist = next_worklist
    next_worklist = set()
    round_counter += 1