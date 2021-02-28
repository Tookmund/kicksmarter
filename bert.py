# String - user title, String Array - Category Titles

def data_processing(user_title, projects_list):

    projects_list.insert(0, user_title)
    projects_list = projects_list[:120]

    vectorizer = Vectorizer()
    vectorizer.bert(projects_list)
    vectors_bert = vectorizer.vectors

    valuelist = []
    for i in range(len(projects_list)):
        dist_1 = spatial.distance.cosine(vectors_bert[0], vectors_bert[i])
        valuelist.append(dist_1 - 1)

    top5 = sorted(valuelist)[:6]
    for i in range(1, 6):
        index = valuelist.index(top5[i])
        # print(projects_list[index], top4[i])
    
    return top5

            