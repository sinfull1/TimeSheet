from git import Repo,remote


def gitPull(gitHubLoc,repotCheckout):
    repoLocal = Repo(repotCheckout)
    origin = repo.remote(name='origin')
    origin.fetch()
    print(origin.refs[0])
    #origin.pull(origin.refs[0].remote_head)

gitHubLoc = 'git@github.com:tiger-syntex/TimeSheet.git'
repotCheckout = 'H:\Repos\MohitYadavGitHub\TimeSheetV2\TimeSheet'
gitPull(gitHubLoc,repotCheckout)
