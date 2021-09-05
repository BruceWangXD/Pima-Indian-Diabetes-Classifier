import sys
import math


def open_file(file_name):
    f=open(file_name)
    all_lines=f.readlines()

    result=[]
    for i in all_lines:
        i=i.strip().split(',')
        result+=i
    
    for i in result:
        for j in i:
            try:
                j=float(j)
            except:
                pass

    
    
    return result

#print(open_file('training.txt'))
#print(open_file('testing.txt'))

def knn(k,training,testing):
    
    i=0
    num_of_attributes=0
    while i<len(training):
        if training[i]=='yes' or training[i]=='no':
            num_of_attributes=i
            break
        i+=1
    
    num_of_group_training=len(training)//(num_of_attributes+1)
    #print(num_of_group)


    training_here=[]
    
    
    i=0
    while i <num_of_group_training:#-1
        training_here.append([])
        j=0
        while j<num_of_attributes+1:
            try:
                training_here[i].append(float(training[j+(1+num_of_attributes)*i]))
            except:
                training_here[i].append(training[j+(1+num_of_attributes)*i])
            j+=1

        i+=1

    #print(training_here)



    num_of_group_testing=len(testing)//(num_of_attributes)
    #print(num_of_group_testing)

    testing_here=[]
    i=0
    while i<num_of_group_testing:
        testing_here.append([])
        j=0
        while j<num_of_attributes:
            testing_here[i].append(float(testing[j+num_of_attributes*i]))
            j+=1
        i+=1


    # print(training_here)
    # print('test')
    # print(testing_here)
    
    for one_testing in testing_here:

        all_dist=[]
        yes_or_no=[]

        
        all_dist,yes_or_no=e_dist(one_testing,training_here,num_of_attributes)
            #print(distance)
        
        sorted_all_dist=[]
        for dist_dist in all_dist:
            sorted_all_dist.append(dist_dist)
        
        sorted_all_dist.sort()

        

        
        i=0
        compare_dist=[]
        while i<k:
            j=0
            while j< num_of_group_training:
                if all_dist[j]==sorted_all_dist[i]:
                    compare_dist.append(j)
                j+=1
            i+=1

        
        num_of_yes=0
        num_of_no=0

        for one_dist in compare_dist:

            if yes_or_no[one_dist]=='yes':
                num_of_yes+=1
            else:
                num_of_no+=1
        
        if num_of_yes>=num_of_no:
            print('yes')
        else:
            print('no')
            


        #print(sorted_all_dist)


def e_dist(one_testing,training_here,num_of_attributes):
    all_dist=[]
    yes_or_no=[]
    
    for one_training in training_here:
            
        distance=0
        i=0
        while i<num_of_attributes:
            distance+=((one_testing[i])-(one_training[i]))*((one_testing[i])-(one_training[i]))
            i+=1
        distance=math.sqrt(distance)
        all_dist.append(distance)
        yes_or_no.append(one_training[num_of_attributes])

    return all_dist,yes_or_no







def nb(training,testing):
    
    i=0
    num_of_attributes=0
    while i<len(training):
        if training[i]=='yes' or training[i]=='no':
            num_of_attributes=i
            break
        i+=1
    
    num_of_group_training=len(training)//(num_of_attributes+1)
    #print(num_of_group)


    training_here=[]
    
    
    i=0
    while i <num_of_group_training:#-1
        training_here.append([])
        j=0
        while j<num_of_attributes+1:
            try:
                training_here[i].append(float(training[j+(1+num_of_attributes)*i]))
            except:
                training_here[i].append(training[j+(1+num_of_attributes)*i])
            j+=1

        i+=1

    #print(training_here)

    num_of_group_testing=len(testing)//(num_of_attributes)
    #print(num_of_group_testing)

    testing_here=[]
    i=0
    while i<num_of_group_testing:
        testing_here.append([])
        j=0
        while j<num_of_attributes:
            testing_here[i].append(float(testing[j+num_of_attributes*i]))
            j+=1
        i+=1


    training_yes=[]
    training_no=[]


    for one_training in training_here:
        add_list=[]
        
        j=0
        while j<num_of_attributes:
            add_list.append(one_training[j])
            j+=1
        
        if one_training[num_of_attributes]=='yes':
            training_yes.append(add_list)
        else:
            training_no.append(add_list)

    all_mean_yes=[]
    all_mean_no=[]
    all_std_yes=[]
    all_std_no=[]


    all_mean_yes,all_std_yes=get_all_mean_std(num_of_attributes,training_yes)
    all_mean_no,all_std_no=get_all_mean_std(num_of_attributes,training_no)

   
    # print(all_mean_no)
    # print(all_std_no)

    l_y=len(training_yes)
    l_n=len(training_no)

    p_y=l_y/(l_y+l_n)
    p_n=l_n/(l_n+l_y)

    p_y_all=[]
    p_n_all=[]

    p_y_all=get_p_y_n(testing_here,num_of_attributes,all_mean_yes,all_std_yes)
    
    
    
    p_n_all=get_p_y_n(testing_here,num_of_attributes,all_mean_no,all_std_no)

    

   


    i=0
    while i<num_of_group_testing:
        p_y_all_1=p_y_all[num_of_attributes*i:num_of_attributes*i+num_of_attributes]
        p_n_all_1=p_n_all[num_of_attributes*i:num_of_attributes*i+num_of_attributes]

        p_yyy=get_p(p_y,p_y_all_1)
        p_nnn=get_p(p_n,p_n_all_1)

        


        if (p_yyy>=p_nnn):
            print('yes')
        else:
            print('no')


        i+=1
    
    
    return None

def get_p_y_n(testing_here,num_of_attributes,all_mean,all_std):
    p_all=[]
    

    for one_testing in testing_here:
        i=0
        while i < num_of_attributes:
            
            p_y_here=math.exp(- (one_testing[i]-all_mean[i])*(one_testing[i]-all_mean[i])/ (2 * all_std[i]*all_std[i]))/(all_std[i] * math.sqrt(2*math.pi))
            p_all.append(p_y_here)

            


            i+=1
       
    return p_all
    
    
    
    
def get_p(p_initial,p_list):
    for i in p_list:
        p_initial*=i
    return p_initial







def get_all_mean_std(num_of_attributes,here_list):
    all_mean=[]
    all_std=[]


    i=0
    while i<num_of_attributes:
        
        num_yes_g=len(here_list)
        sum=0
        j=0
        while j<num_yes_g:
            sum+=here_list[j][i]
            j+=1

        #print(sum)
        sum_mean=sum/num_yes_g

        #print(sum_mean)

        std =0
        j=0
        while j<num_yes_g:
            std+=(here_list[j][i] - sum_mean)*(here_list[j][i] - sum_mean)
            j+=1
        
        #print(std)

        std_dev=math.sqrt(std/(num_yes_g-1))


        all_mean.append(sum_mean)
        all_std.append(std_dev)

        i+=1


    return all_mean,all_std


    



        







#nb(open_file('training.txt'),open_file('testing.txt'))




if len(sys.argv)!=4:
    exit()


try:
    training_training=open_file(sys.argv[1])
    testing_testing=open_file(sys.argv[2])
except:
    exit()

if 'NN' in sys.argv[3]:
    try:
        k_k=int(sys.argv[3][0])
    except:
        exit()
    
    knn(k_k,training_training,testing_testing)

if sys.argv[3]=='NB':
    nb(training_training,testing_testing)



