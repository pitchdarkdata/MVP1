/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Probot} app
 * 
 * 
 * 
 */
try {
  module.exports = (app) => {
    // Your code here
    let outPutReviewers =[];
    app.log.info(typeof outPutReviewers )
    let  final=[];
    let result ='';
    app.log.info("Yay, the app was loaded!");
    app.on("pull_request.opened", async (context) => {
        const data = context.payload;
        // reading data from github api 
        
        const clone_url =data.repository?.clone_url;
        const source = data.pull_request.head.ref;
        const destination = data.pull_request.base.ref;
        const commit = data.pull_request.head.sha;
        const repo_name = data.repository?.name;
    
        const mockDataSending ={
          'repo_url' : clone_url,
          'source' : source,
          'destination': destination,
          'commit':commit,
          'repo_name' : repo_name,
        }
    
        let stringifiedData = JSON.stringify(mockDataSending);
    
        const {spawn} = require('child_process');
    
        const childPython = spawn('python3', ['./reviewer.py', stringifiedData]);
        //const childPython = spawn('python', ['--version'])
        childPython.stdout.on('data', function (data)  {
            console.log(`stdOut: ${data}`);
            result="";
            result+=data.toString();
            
        })
        childPython.stderr.on('data', (data) => {
          app.log.info(`stderr: ${data}`);
        })
    
        childPython.on('close', (code) => {
          app.log.info(`child process exited with code: ${code}`);
          result=result.replace(/[^a-zA-Z0-9 ]/g, "");
          app.log.info(`result: ${result}`);
          final=result.split(" ");
          for(let i=0; i<final.length;i++)
          {
            outPutReviewers.push(final[i]);
          }
          const outPutReviewer = outPutReviewers;
          console.log(`final: ${outPutReviewers instanceof Array}`);
          
          //adding reviewers
          const reviewer = context.pullRequest({
          reviewers:outPutReviewer
          });
      
        context.octokit.rest.pulls.requestReviewers(reviewer);
    
        return context.octokit.pulls.createReviewComment("done");
    
      })
  
    process.on('unhandledRejection', function(err) {
        console.log(err);
    });
      
    
    })
    app.onError(async (err) => {
      console.log(err);
    })
  };
}
catch(e)
{
  console.log(e);
}

