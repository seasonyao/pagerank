#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include<sstream>
#include<algorithm>

using namespace std;

vector<int> SAM_x;
vector<int> SAM_y;
vector<int> all_Page;
vector<int> a_P_count;
vector<double> pageRank;
vector<double> lastRank;
vector<double> tempRank;
vector<int>::iterator it;
vector<double>::iterator it_d;
double** GM_matrix;
double** D_matrix;
double** A_matrix;
int pageNum;
const double Alpha=0.8;

int str2int(const string &string_temp) ;
vector<string> split(const string &str,const string &pattern);
bool readTxt(string file);
bool matrix_initialize();
bool begin_iterate();
bool Comp(const int &a,const int &b);
int main(){
	//读取文件，构建SAMx y value pageRank lastRank tempRank
	readTxt("WikiData_test.txt");
	//初始化GM D A
	matrix_initialize();
	//正式迭代
	begin_iterate();

	system("pause");
}






int str2int(const string &string_temp)  
{  
	int int_temp;
    stringstream stream(string_temp);  
    stream>>int_temp;  
	return int_temp;
}  
vector<string> split(const string &str,const string &pattern)
{
    //const char* convert to char*
    char * strc = new char[strlen(str.c_str())+1];
    strcpy(strc, str.c_str());
    vector<string> resultVec;
    char* tmpStr = strtok(strc, pattern.c_str());
    while (tmpStr != NULL)
    {
        resultVec.push_back(string(tmpStr));
        tmpStr = strtok(NULL, pattern.c_str());
    }

    delete[] strc;

    return resultVec;
}
bool readTxt(string file)
{
    ifstream infile; 
    infile.open(file.data());   //将文件流对象与文件连接起来  

    string s;
	vector<string> temp;
	vector<int>::iterator ret;
    while(getline(infile,s))
    {
		temp=split(s,"	");
		SAM_x.push_back(str2int(temp[0]));
		SAM_y.push_back(str2int(temp[1]));
		ret = find(all_Page.begin(), all_Page.end(), str2int(temp[0]));
		if(ret==all_Page.end()){
			all_Page.push_back(str2int(temp[0]));
		}
		ret = find(all_Page.begin(), all_Page.end(), str2int(temp[1]));
		if(ret==all_Page.end()){
			all_Page.push_back(str2int(temp[1]));
		}
    }
	vector<int>::iterator p = max_element(all_Page.begin(), all_Page.end());
    pageNum=*p;

	for(int i=0;i<pageNum;i++){
		pageRank.push_back(1.0/pageNum);
		lastRank.push_back(1.0/pageNum);
		tempRank.push_back(1.0/pageNum);
	}
    infile.close();             //关闭文件输入流 
	return true;
}
bool matrix_initialize(){
	//构建GM、D、A矩阵
	GM_matrix=new double*[pageNum];
	D_matrix=new double*[pageNum];
	A_matrix=new double*[pageNum];
	for(int i=0;i<pageNum;i++){
		*(GM_matrix+i)=new double[pageNum];
		*(D_matrix+i)=new double[pageNum];
		*(A_matrix+i)=new double[pageNum];
		for(int j=0;j<pageNum;j++){
			GM_matrix[i][j]=0.0;
			D_matrix[i][j]=1.0/pageNum;
			A_matrix[i][j]=0.0;
		}
	}
	//求出各个page向外指出多少次，用来更新后面的矩阵
	int num = 0;

	for(int i=0;i<all_Page.size();i++){
		num= count(SAM_x.begin(),SAM_x.end(),all_Page[i]);//统计每个值出现的次数
		a_P_count.push_back(num);
	}
	
	//更新GM矩阵
	int count=0;
	for(int i=0;i<SAM_x.size();i++){
		it=find(all_Page.begin(),all_Page.end(),SAM_y[count]);
		auto temp1=distance(std::begin(all_Page), it);
		it=find(all_Page.begin(),all_Page.end(),SAM_x[i]);
		auto temp2=distance(std::begin(all_Page), it);
		//cout<<temp1<<endl<<temp2<<endl;
		GM_matrix[temp1][temp2]=1.0/a_P_count[temp2];
		count++;
	}

	//更新A矩阵
	for(int i=0;i<pageNum;i++)
		for(int j=0;j<pageNum;j++)
			A_matrix[i][j]=GM_matrix[i][j]*Alpha+D_matrix[i][j]*(1.0-Alpha);

	return true;
}
bool begin_iterate(){
	ofstream outfile("record_full_matrix.txt");
	ofstream out("rank.txt");
	while(true){
		for(int i=0;i<pageNum;i++){
			double sum=0.0;
			for(int j=0;j<pageNum;j++)
				sum=sum+A_matrix[i][j]*lastRank[j];
			pageRank[i]=sum;
		}
		int flag=0;
		for(int i=0;i<pageNum;i++){
			if(abs(lastRank[i]-pageRank[i])!=0)
				flag=1;
			lastRank[i]=pageRank[i];
		}
		if(flag==0)
			break;
		for(int i=0;i<pageNum;i++){
			tempRank[i]=pageRank[i];
		}
		sort(tempRank.begin(),tempRank.end());
		reverse(tempRank.begin(),tempRank.end());
		for(int i=0;i<4;i++){
			it_d = find(pageRank.begin(),pageRank.end(),tempRank[i]);
			auto temp=distance(std::begin(pageRank), it_d);
			pageRank[temp]=0;
			cout<<"第"<<i+1<<"名:	"<<temp+1<<endl;
		}
		cout<<"------------------------------------"<<endl;
		for(int i=0;i<pageNum;i++)
			outfile<<lastRank[i]<<"\t";
		outfile<<endl<<"---------------------"<<endl;
	}
	outfile.close();
	out.close();
	return true;
}
