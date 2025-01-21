@Library('StanUtils')
import org.stan.Utils

def utils = new org.stan.Utils()

pipeline {
    agent none
    options {
        skipDefaultCheckout()
        preserveStashes(buildCount: 7)
        parallelsAlwaysFailFast()
        buildDiscarder(logRotator(numToKeepStr: '20', daysToKeepStr: '30'))
    }
    environment {
        GIT_AUTHOR_NAME = 'Stan Jenkins'
        GIT_AUTHOR_EMAIL = 'mc.stanislaw@gmail.com'
        GIT_COMMITTER_NAME = 'Stan Jenkins'
        GIT_COMMITTER_EMAIL = 'mc.stanislaw@gmail.com'
        GITHUB_TOKEN = credentials('6e7c1e8f-ca2c-4b11-a70e-d934d3f6b681')
    }
    stages {
        
        stage("Update docs") {
            agent {
                docker {
                    image 'alpine/git'
                    label 'linux && triqs'
                    args "--entrypoint=''"
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'a630aebc-6861-4e69-b497-fd7f496ec46b',
                    usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                    sh """
                        git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/stan-dev/docs.git

                        cd docs

                        git config user.email "mc.stanislaw@gmail.com"
                        git config user.name "Stan Jenkins"
                        git config auth.token ${GITHUB_TOKEN}

                        git checkout master
                        git pull origin master
                        git submodule update --init --recursive --remote

                        cd src/quarto-config
                        git checkout origin/main
                        git pull origin main
                        cd ../..

                        git submodule update --init --recursive --remote
                    """
                    script {
                        env.COMMIT_HASH = sh (
                            script: 'cd docs/src/quarto-config && git rev-parse --short HEAD && cd ../..',
                            returnStdout: true
                        )
                    }
                    sh """
                        cd docs
                        if [[ -n "`git status -s`" ]]; then
                            git add .
                            git commit -m "Updating submodule quarto to ${env.COMMIT_HASH.trim()}"
                            git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/stan-dev/docs.git master
                        fi
                    """
                }
            }
            post { always { deleteDir() } }
        }

        stage("Update stan-dev.github.io") {
            agent {
                docker {
                    image 'mrnonz/alpine-git-curl'
                    label 'linux && triqs'
                    args "--entrypoint=''"
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'a630aebc-6861-4e69-b497-fd7f496ec46b',
                    usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                    sh """
                        git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/stan-dev/stan-dev.github.io.git

                        cd stan-dev.github.io

                        git config user.email "mc.stanislaw@gmail.com"
                        git config user.name "Stan Jenkins"
                        git config auth.token ${GITHUB_TOKEN}

                        git checkout master
                        git pull origin master
                        git submodule update --init --recursive --remote

                        cd quarto-config
                        git checkout origin/main
                        git pull origin main
                        cd ../

                        git submodule update --init --recursive --remote

                        git status
                        pwd

                    """
                    script {
                        env.COMMIT_HASH = sh (
                            script: 'cd stan-dev.github.io/quarto-config && git rev-parse --short HEAD && cd ../..',
                            returnStdout: true
                        )
                    }
                    sh """
                        pwd
                        cd stan-dev.github.io
                        if [[ -n "`git status -s`" ]]; then
                            git checkout -b quarto-${env.COMMIT_HASH.trim()}
                            git add .
                            git commit -m "Updating submodule quarto to ${env.COMMIT_HASH.trim()}"
                            git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/stan-dev/stan-dev.github.io.git quarto-${env.COMMIT_HASH.trim()}
                            curl -s -H "Authorization: token ${GITHUB_TOKEN}" -X POST -d '{"title": "Updating submodule quarto to ${env.COMMIT_HASH.trim()}", "base":"master", "head":"quarto-${env.COMMIT_HASH.trim()}", "body":"Updating submodule quarto to ${env.COMMIT_HASH.trim()}"}' "https://api.github.com/repos/stan-dev/stan-dev.github.io/pulls"
                        fi
                    """
                }
            }
            post { always { deleteDir() } }
        }

    }
    // post {
    //     success { script { utils.mailBuildResults("SUCCESSFUL") } }
    //     unstable { script { utils.mailBuildResults("UNSTABLE", "stan-buildbot@googlegroups.com") } }
    //     failure { script { utils.mailBuildResults("FAILURE", "stan-buildbot@googlegroups.com") } }
    // }
}