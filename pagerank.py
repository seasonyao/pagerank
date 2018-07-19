import time
import sys   
sys.setrecursionlimit(1000000000) #设置递归内陷的最大值


#QuickSort根据x为xy两个list都进行快排
def QuickSort(myList,myListy,start,end):
    #判断low是否小于high,如果为false,直接返回
    if start < end:
        i,j = start,end
        #设置基准数
        base = myList[i]
        tempy= myListy[i]

        while i < j:
            #如果列表后边的数,比基准数大或相等,则前移一位直到有比基准数小的数出现
            while (i < j) and (myList[j] >= base):
                j = j - 1

            #如找到,则把第j个元素赋值给第个元素i,此时表中i,j个元素相等
            myList[i] = myList[j]
            myListy[i]=myListy[j]

            #同样的方式比较前半区
            while (i < j) and (myList[i] <= base):
                i = i + 1

            myList[j] = myList[i]
            myListy[j]=myListy[i]
        #做完第一轮比较之后,列表被分成了两个半区,并且i=j,需要将这个数设置回base
        myList[i] = base
        myListy[i]=tempy

        #递归前后半区
        QuickSort(myList,myListy, start, i - 1)
        QuickSort(myList,myListy, j + 1, end)
    return myList


Alpha=0.85


all_SAM_x=[]#sparse_adjacency_matrix_x
all_SAM_y=[]#sparse_adjacency_matrix_y
all_pages = []
temp_all_pages=[]
temp_all_SAM_x=[]
temp_all_SAM_y=[]
pageRank=[]
lastRank=[]
GM_matrix=[]
D_matrix=[]
A_matrix=[]
live_end=[]
dead_end=[]
SAM_x=[]
SAM_y=[]
SAM_value=[]
dead_SAM_value=[]
dead_x=[]
dead_y=[]
last_live_end=[]
lastRank=[]
pageRank=[]
allPageRank=[]

f = open('WikiData.txt',encoding='UTF-8')
line = f.readline()
while line:
    temp_x,temp_y=line.split('	')
    all_SAM_x.append(int(temp_x))
    all_SAM_y.append(int(temp_y))
    temp_all_SAM_x.append(int(temp_x))
    temp_all_SAM_y.append(int(temp_y))
    if int(temp_x) not in all_pages:
    	all_pages.append(int(temp_x))
    	temp_all_pages.append(int(temp_x))
    	last_live_end.append(int(temp_x))
    if int(temp_y) not in all_pages:
    	all_pages.append(int(temp_y))
    	temp_all_pages.append(int(temp_y))
    	last_live_end.append(int(temp_y))
    line = f.readline()
f.close()
print(1)
#为了避免dead end递归把deadend拿掉
while(1):
	print(dead_end)
	print(len(last_live_end))
	print(len(live_end))
	if len(last_live_end)==len(live_end):
		break
	last_live_end=[]
	for i in live_end:
		last_live_end.append(i)
	live_end=[]
	SAM_x=[]
	SAM_y=[]
	for i in temp_all_pages:
		if i in temp_all_SAM_x:
			live_end.append(i)
		else:
			dead_end.append(i)
	for i in range(0,len(temp_all_SAM_x)):
		if temp_all_SAM_x[i] in live_end:
			SAM_x.append(temp_all_SAM_x[i])
			SAM_y.append(temp_all_SAM_y[i])
		else:
			dead_x.append(temp_all_SAM_x[i])
			dead_y.append(temp_all_SAM_y[i])
	temp_all_pages=[]
	temp_all_SAM_x=[]
	temp_all_SAM_y=[]
	for i in live_end:
		temp_all_pages.append(i)
	for i in range(0,len(all_SAM_x)):
		if all_SAM_x[i] in temp_all_pages and all_SAM_y[i] in temp_all_pages:
			temp_all_SAM_x.append(all_SAM_x[i])
			temp_all_SAM_y.append(all_SAM_y[i])

for i in range(0,len(all_SAM_x)):
	if all_SAM_x[i] in dead_end or all_SAM_y[i] in dead_end:
		dead_x.append(all_SAM_x[i])
		dead_y.append(all_SAM_y[i])

print(2)
live_end.sort()
pageNum=len(live_end)
allpageNum=len(all_pages)


'''
for i in range(0,pageNum):
	pageRank.append(1/pageNum)
	lastRank.append(1/pageNum)


#先按全矩阵的做一遍
#横坐标表示目的点，纵坐标表示源点

#初始化GM、D、A矩阵，算好D矩阵
for i in range(0,pageNum):
	temp1=[]
	temp2=[]
	temp3=[]
	for j in range(0,pageNum):
		temp1.append(0)
		temp2.append(1/pageNum)
		temp3.append(0)
	GM_matrix.append(temp1)
	D_matrix.append(temp2)
	A_matrix.append(temp3)

#求出各个page向外指出多少次，用来更新后面的矩阵
occur_count = {}
for item in SAM_x:
    occur_count[item] = occur_count.get(item, 0) + 1

#更新GM矩阵

occur=[]
for i in occur_count.values():
	occur.append(i)

count=0
for i in SAM_x:
	GM_matrix[live_end.index(SAM_y[count])][live_end.index(i)]=1/occur[live_end.index(i)]
	count=count+1

#计算A矩阵
for i in range(0,pageNum):
	for j in range(0,pageNum):
		A_matrix[i][j]=GM_matrix[i][j]*Alpha+D_matrix[i][j]*(1-Alpha)

#正式迭代
with open('record_full_matrix.txt','w+',encoding='UTF-8') as ff:
	while(1):
		for i in range(0,pageNum):
			sum=0
			for j in range(0,pageNum):
				sum=sum+A_matrix[i][j]*lastRank[j]
			pageRank[i]=sum
		ff.write(str(pageRank))
		ff.write('\n')
		ff.write('-----------------------------------------------------')
		ff.write('\n')
		flag=0
		for i in range(0,pageNum):
			if abs(lastRank[i]-pageRank[i])>0.0000001:
				flag=1
			lastRank[i]=pageRank[i]
		if flag==0:
			break
		print("---------------------------------------------")
		print("第一名"+str(1+pageRank.index(max(pageRank))))
		pageRank[pageRank.index(max(pageRank))]=0
		print("第二名"+str(1+pageRank.index(max(pageRank))))
		pageRank[pageRank.index(max(pageRank))]=0
		print("第三名"+str(1+pageRank.index(max(pageRank))))
		pageRank[pageRank.index(max(pageRank))]=0
		print("第四名"+str(1+pageRank.index(max(pageRank))))
		pageRank[pageRank.index(max(pageRank))]=0
		print("第五名"+str(1+pageRank.index(max(pageRank))))
		pageRank[pageRank.index(max(pageRank))]=0
		print("第六名"+str(1+pageRank.index(max(pageRank))))
		pageRank[pageRank.index(max(pageRank))]=0
		print("第七名"+str(1+pageRank.index(max(pageRank))))
		pageRank[pageRank.index(max(pageRank))]=0
		print("第八名"+str(1+pageRank.index(max(pageRank))))
		pageRank[pageRank.index(max(pageRank))]=0
		print("第九名"+str(1+pageRank.index(max(pageRank))))
		pageRank[pageRank.index(max(pageRank))]=0
		print("第十名"+str(1+pageRank.index(max(pageRank))))
print('结束1')

with open('full_matrix_rank_result.txt','w+',encoding='UTF-8') as ff:
	ff.write("第一名"+str(1+lastRank.index(max(lastRank)))+"\n")
	lastRank[lastRank.index(max(lastRank))]=0
	ff.write("第二名"+str(1+lastRank.index(max(lastRank)))+"\n")
	lastRank[lastRank.index(max(lastRank))]=0
	ff.write("第三名"+str(1+lastRank.index(max(lastRank)))+"\n")
	lastRank[lastRank.index(max(lastRank))]=0
	ff.write("第四名"+str(1+lastRank.index(max(lastRank)))+"\n")
	lastRank[lastRank.index(max(lastRank))]=0
	ff.write("第五名"+str(1+lastRank.index(max(lastRank)))+"\n")
	lastRank[lastRank.index(max(lastRank))]=0
	ff.write("第六名"+str(1+lastRank.index(max(lastRank)))+"\n")
	lastRank[lastRank.index(max(lastRank))]=0
	ff.write("第七名"+str(1+lastRank.index(max(lastRank)))+"\n")
	lastRank[lastRank.index(max(lastRank))]=0
	ff.write("第八名"+str(1+lastRank.index(max(lastRank)))+"\n")
	lastRank[lastRank.index(max(lastRank))]=0
	ff.write("第九名"+str(1+lastRank.index(max(lastRank)))+"\n")
	lastRank[lastRank.index(max(lastRank))]=0
	ff.write("第十名"+str(1+lastRank.index(max(lastRank)))+"\n")

'''


#coo处理稀疏矩阵

#处理SAM_value的值
QuickSort(SAM_x,SAM_y,0,len(SAM_x)-1)

#求出各个page向外指出多少次，用来更新后面的矩阵
occur_count = {}
for item in SAM_x:
    occur_count[item] = occur_count.get(item, 0) + 1

#这里可以得到GM矩阵的value
#SAM_value=[]
#for i in range(0,len(SAM_x)):
#	SAM_value.append(1/occur_count[SAM_x[i]])

#这里可以得到A矩阵的value,相当于A矩阵没被记录下来的就默认是（1-Alpha）/pageNum
for i in range(0,len(SAM_x)):
	SAM_value.append(Alpha/occur_count[SAM_x[i]]+(1-Alpha)/pageNum)

#初始化pageRank向量
for i in range(0,pageNum):
	pageRank.append(1/pageNum)
	lastRank.append(1/pageNum)

print(3)
#正式迭代，计算方法是每次先默认所有都是（1-Alpha）/pageNum 乘以 rank向量对应的元素，然后遍历SAM list把对应的改正
with open('record_sparse_matrix.txt','w+',encoding='UTF-8') as ff:
	with open('coo_rank_result.txt','w+',encoding='UTF-8') as f1:
		while(1):
			#首先算出本次迭代默认的一行值为sum
			sum=0
			for j in range(0,pageNum):
				sum=sum+lastRank[j]*(1-Alpha)/pageNum
			for j in range(0,pageNum):
				pageRank[j]=sum
			#然后利用默认值sum和SAM list来对rank的每个值进行对应的修改
			for i in range(0,len(SAM_x)):
				pageRank[live_end.index(SAM_y[i])]=pageRank[live_end.index(SAM_y[i])]-lastRank[live_end.index(SAM_x[i])]*(1-Alpha)/pageNum+lastRank[live_end.index(SAM_x[i])]*SAM_value[i]
			#time.sleep(5)
			ff.write(str(pageRank))
			ff.write('\n')
			ff.write('-----------------------------------------------------')
			ff.write('\n')
			flag=0
			print(pageRank)
			for i in range(0,pageNum):
				if abs(lastRank[i]-pageRank[i])>0.000000000000000001:
					flag=1
				lastRank[i]=pageRank[i]
			if flag==0:
				break


			#for i in range(0,100):
			#	f1.write(str(1+lastRank.index(max(lastRank)))+"\t"+str(max(lastRank))+"\n")
			#	lastRank[lastRank.index(max(lastRank))]=0

			temp_sum=0
			for i in range(0,pageNum):
				lastRank[i]=pageRank[i]
				temp_sum+=pageRank[i]
			print(temp_sum)

#将live end的排名算完这时候再加上dead end的
#处理all_SAM_value的值
QuickSort(all_SAM_x,all_SAM_y,0,len(all_SAM_x)-1)

#求出各个page向外指出多少次，用来更新后面的矩阵
occur_count = {}
for item in all_SAM_x:
    occur_count[item] = occur_count.get(item, 0) + 1


# 1/allpageNum

for i in range(0,len(dead_x)):
	dead_SAM_value.append(1/occur_count[dead_x[i]])
#算出各个算出各个dead end的pagerank值来
dead_end=list(reversed(dead_end))



for i in pageRank:
	allPageRank.append(i)

for i in range(0,len(dead_end)):
	score=0
	for j in range(0,len(dead_x)):
		if dead_y[j] == dead_end[i]:
			score+=dead_SAM_value[j]*allPageRank[live_end.index(dead_x[j])]
	allPageRank.append(score)
	live_end.append(dead_end[i])


#输出排名到对应文件里

with open('coo_rank_result.txt','w+',encoding='UTF-8') as ff:
	for i in range(0,100):
		ff.write(str(1+allPageRank.index(max(allPageRank)))+"\t"+str(max(allPageRank))+"\n")
		allPageRank[allPageRank.index(max(allPageRank))]=0

print('结束2')


'''
#block_strip algorithm
temp_y=[]
for i in SAM_y:
	temp_y.append(i)
#处理SAM_value的值
QuickSort(temp_y,SAM_x,0,len(SAM_y)-1)
QuickSort(SAM_y,SAM_value,0,len(SAM_y)-1)

#求出各个page被指了多少次
occur_count = {}
for item in SAM_y:
    occur_count[item] = occur_count.get(item, 0) + 1


M=[]
curr=0
#进行block的操作
#首先为了减小占据的空间coo模式改成sdd模式
for i in range(0,len(occur_count)):
	temp_samy=SAM_y[curr]
	temp_occur_count=occur_count[SAM_y[curr]]
	M.append(temp_samy)
	M.append(temp_occur_count)
	for j in range(0,temp_occur_count):
		M.append(SAM_x[curr])
		M.append(SAM_value[curr])
		curr+=1
#所以现在的M可以被假设成为磁盘中的连续块，例子：
#[1 , 1, 2, 0.45, 2, 2, 1, 0.3167, 4, 0.45, 3, 3, 1, 0.3167, 4, 0.45, 3, 0.85, 4, 2, 2, 0.45, 1, 0.3167]

#假定每次读入内存的pagerank大小为100
block_size=100

#初始化pageRank向量
lastRank=[]
pageRank=[]

for i in range(0,pageNum):
	pageRank.append(1/pageNum)
	lastRank.append(1/pageNum)

#正式迭代，每次读入block_size个strip
with open('record_block_strip_matrix.txt','w+',encoding='UTF-8') as ff:
	while(1):
		curr=0#用来模拟在磁盘里的探针

		#首先算出本次迭代默认的一行值为sum后面会用,这里会遍历一次lastrank
		sum=0
		for j in range(0,pageNum):
			sum=sum+lastRank[j]*(1-Alpha)/pageNum

		#开始对每个block strip进行操作
		for n in range(0,int(pageNum/block_size)):
			#首先把本次memory里的pagerank lastrank和strip都装进内存
			#将M恢复成coo的模式便于计算
			base=n*block_size#本次block的基始点
			coo_x=[]
			coo_y=[]
			coo_value=[]
			memory_pagerank=[]
		
			#模拟读取内存
			for i in range(0,block_size):
				memory_pagerank.append(lastRank[base+i])
				des=M[curr]
				if des>=base+1 and des<base+1+block_size:
					curr+=1
					num=M[curr]
					curr+=1
					for j in range(0,num):
						coo_x.append(M[curr])
						curr+=1
						coo_y.append(des)
						coo_value.append(M[curr])
						curr+=1


			#接下来就可以使用之前的方法来进行这一小块的计算pagerank
			for j in range(0,block_size):
				memory_pagerank[j]=sum

			#然后利用默认值sum和SAM list来对rank的每个值进行对应的修改
			#print('-------------------')
			#print(len(coo_y))
			for i in range(0,len(coo_y)):
				memory_pagerank[coo_y[i]-1-base]=memory_pagerank[coo_y[i]-1-base]-lastRank[coo_x[i]-1]*(1-Alpha)/pageNum+lastRank[coo_x[i]-1]*coo_value[i]

			#将修正后的结果输出给pagerank
			for x in range(0,block_size):
				pageRank[base+x]=memory_pagerank[x]

		#接下来处理最后不足block_size的一块
		coo_x=[]
		coo_y=[]
		coo_value=[]
		memory_pagerank=[]
		base=int(pageNum/block_size)*block_size
		#模拟读取内存
		for i in range(0,pageNum%block_size):
			memory_pagerank.append(lastRank[base+i])
			try:
				des=M[curr]
				if des>=base+1 and des<base+1+pageNum%block_size:
					curr+=1
					num=M[curr]
					curr+=1
					for j in range(0,num):
						coo_x.append(M[curr])
						curr+=1
						coo_y.append(des)
						coo_value.append(M[curr])
						curr+=1
			except IndexError:
				pass

		#接下来就可以使用之前的方法来进行这一小块的计算pagerank
		for j in range(0,pageNum%block_size):
			memory_pagerank[j]=sum

		#然后利用默认值sum和SAM list来对rank的每个值进行对应的修改
		for i in range(0,len(coo_x)):
			memory_pagerank[coo_y[i]-1-base]=memory_pagerank[coo_y[i]-1-base]-lastRank[coo_x[i]-1]*(1-Alpha)/pageNum+lastRank[coo_x[i]-1]*coo_value[i]

		#将修正后的结果输出给pagerank
		for x in range(0,pageNum%block_size):
			pageRank[base+x]=memory_pagerank[x]


		#相当于一次迭代的结束，接下来进行输出扫尾操作
		ff.write(str(pageRank))
		ff.write('\n')
		ff.write('-----------------------------------------------------')
		ff.write('\n')
		flag=0
		for i in range(0,pageNum):
			if abs(lastRank[i]-pageRank[i])>0.00000000001:
				flag=1
			lastRank[i]=pageRank[i]
		if flag==0:
			break


#将live end的排名算完这时候再加上dead end的
#处理all_SAM_value的值
QuickSort(all_SAM_x,all_SAM_y,0,len(all_SAM_x)-1)

#求出各个page向外指出多少次，用来更新后面的矩阵
occur_count = {}
for item in all_SAM_x:
    occur_count[item] = occur_count.get(item, 0) + 1


# 1/allpageNum

for i in range(0,len(dead_x)):
	dead_SAM_value.append(1/occur_count[dead_x[i]])
#算出各个算出各个dead end的pagerank值来
dead_end=list(reversed(dead_end))



for i in pageRank:
	allPageRank.append(i)

for i in range(0,len(dead_end)):
	score=0
	for j in range(0,len(dead_x)):
		if dead_y[j] == dead_end[i]:
			score+=dead_SAM_value[j]*allPageRank[live_end.index(dead_x[j])]
	allPageRank.append(score)
	live_end.append(dead_end[i])


#输出排名到对应文件里

with open('block_strip_rank_result.txt','w+',encoding='UTF-8') as ff:
	for i in range(0,4):
		ff.write(str(1+allPageRank.index(max(allPageRank)))+"\t"+str(max(allPageRank))+"\n")
		allPageRank[allPageRank.index(max(allPageRank))]=0

print('结束3')
'''