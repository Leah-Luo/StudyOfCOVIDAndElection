# Study of COVID-19 and Election

## Abstract 
<p>2020 must be a memorable year to many Americans. During this year, the United States suffered a severe COVID-19 epidemic. The COVID-19 epidemic has severely affected the lives of many people in the United States. One of our goals is to study the degree of concern and position about the epidemic over time.</p>
<p>As the 2020 presidential election approaches the final poll, discussions on the topics of the election became more and more popular. During the two presidential debates, COVID-19 is one of the most important debate segments. As the debate continues, the discussion among COVID-19 continuously increases on Twitter. Many users post tweets to express different standpoints to the coronavirus pandemic. We are interested in if the election affects the opinions of COVID-19 among individuals whose standpoints might be swayed by the election campaigns.</p>

## Data Collection and Analysis
### Installation
Run the following commands in terminal to install all the packages.
<pre><code> pip install tweepy
 pip install twitter
 pip install nltk
 pip install pandas 
 pip install matplotlib
 pip install emoji
</code></pre>

### Execution
Please use original Dataset.csv file to run Main.py under the source code directory
<ol>
	<li>python3 ExtractTweets.py --------- Extract tweets data into the CSV file at the current time.</li>
	<li>Python3 Main.py		--------- Generate a CSV file with tweets about COVID-19, and start sentiment analysis.</li>
	<li>Node*:The tweets data will be extracted into the CSV file. Since the program can only extract tweets by the current time, if you would like to extract more days data, you probably should run the program every day before starting running the analysis part. All commands should be running in the terminal in the correct directory. The program will generate several figures one by one, please close the pop-out figure in order to continue the execution. </li>
</ol>