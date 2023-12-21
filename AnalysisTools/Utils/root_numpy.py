import uproot
import numexpr as ne
import ast
import itertools
import copy
# This is literally just uproot but I rewrote the root_numpy code so I didnt have to rewrite my entire analysis #
# python3 CategorizedTemplateMaker.py -i ULRun2_22_tagged_signal_trees.txt -p ggH -c Untagged -f 2e2mu -y 2016 -o Testing_Optimal
def tree2array(**kwargs):
    t = None
    branches = None
    top_branch_name = None
    for key, value in kwargs.items():
        if key.lower() == "tree":
            t = value
        elif key.lower() == "branches":
            branches = value[0]
        elif key.lower() == "top_branch_name":
            top_branch_name = value
        else:
            raise Exception("Unable to parse the arguments, check to make sure the arguments are \"tree\" and \"branches\"")

    uproot_tree = uproot.open(t)

    names = [node.id for node in ast.walk(ast.parse(branches)) if isinstance(node, ast.Name)]

    #print("TEST",names,uproot_tree[top_branch_name])
    try:
        Accessed_Branches = uproot_tree[top_branch_name].arrays(names,library="np")
    except:
        print("Checking if the case is an issue")
        single_name_change = itertools.combinations(names,1)
        double_name_change = None
        triple_name_change = None
        quad_name_change = None
        if len(names) >= 2:
            double_name_change = itertools.combinations(names,2)
        if len(names) >= 3:
            triple_name_change = itertools.combinations(names,3)
            print("TRIPLE NAME")
        if len(names) >= 4:
            quad_name_change = itertools.combinations(names,4)
        Not_Solved = True
        while Not_Solved:
            for name in single_name_change:
                new_set = copy.deepcopy(names)
                print("Capitalizing: ",name, " in ",new_set)
                try:
                    new_set[new_set.index(name[0])] = new_set[new_set.index(name[0])].replace("Gen","GEN",1)
                    print("Attempting to try: ",new_set)
                    Accessed_Branches = uproot_tree[top_branch_name].arrays(new_set,library="np")
                except:
                    print("Did not work !")
                else:
                    Accessed_Branches = uproot_tree[top_branch_name].arrays(new_set,library="np")
                    print("Replacing Branch Name after fixing capitalization")
                    branches = branches.replace(name[0],name[0].replace("Gen","GEN",1))
                    print("Succeeded!")
                    Not_Solved = False
            if double_name_change != None:
                for name_pair in double_name_change:
                    new_set = copy.deepcopy(names)
                    print("Capitalizing: ",name_pair)
                    try: 
                        new_set[new_set.index(name_pair[0])]=new_set[new_set.index(name_pair[0])].replace("Gen","GEN",1)
                        new_set[new_set.index(name_pair[1])]=new_set[new_set.index(name_pair[1])].replace("Gen","GEN",1)
                        print("Attempting to try: ",new_set)
                        Accessed_Branches = uproot_tree[top_branch_name].arrays(new_set,library="np")
                    except:
                        print("Did not work!")
                    else:
                        Accessed_Branches = uproot_tree[top_branch_name].arrays(new_set,library="np")
                        branches = branches.replace(name_pair[0],name_pair[0].replace("Gen","GEN",1))
                        branches = branches.replace(name_pair[1],name_pair[1].replace("Gen","GEN",1))
                        print("Succeeded!")
                        Not_Solved = False
            if triple_name_change != None:
                for name_triplet in triple_name_change:
                    new_set = copy.deepcopy(names)
                    print("Capitalizing: ",name_triplet)
                    try: 
                        new_set[new_set.index(name_triplet[0])]=new_set[new_set.index(name_triplet[0])].replace("Gen","GEN",1)
                        new_set[new_set.index(name_triplet[1])]=new_set[new_set.index(name_triplet[1])].replace("Gen","GEN",1)
                        new_set[new_set.index(name_triplet[2])]=new_set[new_set.index(name_triplet[2])].replace("Gen","GEN",1)
                        print("Attempting to try: ",new_set)
                        Accessed_Branches = uproot_tree[top_branch_name].arrays(new_set,library="np")
                    except:
                        print("Did not work!")
                    else:
                        Accessed_Branches = uproot_tree[top_branch_name].arrays(new_set,library="np")
                        branches = branches.replace(name_triplet[0],name_triplet[0].replace("Gen","GEN",1))
                        branches = branches.replace(name_triplet[1],name_triplet[1].replace("Gen","GEN",1))
                        branches = branches.replace(name_triplet[2],name_triplet[2].replace("Gen","GEN",1))
                        print("Succeeded!")
                        Not_Solved = False
            Not_Solved = False       
            
        
    # check if we have to do math !!! #
    operators = ["-","*","+","/"]
    
    doMath = False
    for operator in operators:
        if operator in branches:
            doMath = True

    if doMath:
        return(ne.evaluate(branches, local_dict=Accessed_Branches))
    else:
        return Accessed_Branches[branches]
