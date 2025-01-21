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
                }
            }
            steps {
                /* Pull docs and init submodules */
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/master']],
                          doGenerateSubmoduleConfigurations: false,
                          extensions: [[$class: 'SubmoduleOption',
                                        disableSubmodules: false,
                                        parentCredentials: false,
                                        recursiveSubmodules: true,
                                        reference: '',
                                        trackingSubmodules: false]],
                          submoduleCfg: [],
                          userRemoteConfigs: [[url: "https://github.com/stan-dev/docs.git", credentialsId: 'a630aebc-6861-4e69-b497-fd7f496ec46b']]]
                )

                sh """
                    pushd src/quarto-config > /dev/null
                    git checkout main
                    git pull origin
                    export commit_hash=$(git rev-parse --short main)
                    popd > /dev/null

                    git submodule update --init --recursive
                """

                /* Create Pull Request */
                withCredentials([usernamePassword(credentialsId: 'a630aebc-6861-4e69-b497-fd7f496ec46b',
                    usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                    sh """
                        git config user.email "mc.stanislaw@gmail.com"
                        git config user.name "Stan Jenkins"
                        git config auth.token ${GITHUB_TOKEN}

                        git add .
                        git commit -m "Updating submodule quarto to $commit_hash"
                        git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/stan-dev/docs.git master
                    """
                }
            }
        }

        stage("Update stan-dev.github.io") {
            agent {
                docker {
                    image 'alpine/git'
                    label 'linux && triqs'
                }
            }
            steps {
                /* Pull docs and init submodules */
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/master']],
                          doGenerateSubmoduleConfigurations: false,
                          extensions: [[$class: 'SubmoduleOption',
                                        disableSubmodules: false,
                                        parentCredentials: false,
                                        recursiveSubmodules: true,
                                        reference: '',
                                        trackingSubmodules: false]],
                          submoduleCfg: [],
                          userRemoteConfigs: [[url: "https://github.com/stan-dev/stan-dev.github.io.git", credentialsId: 'a630aebc-6861-4e69-b497-fd7f496ec46b']]]
                )

                sh """
                    pushd quarto-config > /dev/null
                    git checkout main
                    git pull origin
                    export commit_hash=$(git rev-parse --short main)
                    popd > /dev/null

                    git submodule update --init --recursive
                """

                /* Create Pull Request */
                withCredentials([usernamePassword(credentialsId: 'a630aebc-6861-4e69-b497-fd7f496ec46b',
                    usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                    sh """
                        git config user.email "mc.stanislaw@gmail.com"
                        git config user.name "Stan Jenkins"
                        git config auth.token ${GITHUB_TOKEN}

                        git checkout -b quarto-$commit_hash

                        git add .
                        git commit -m "Updating submodule quarto to $commit_hash"
                        git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/stan-dev/stan-dev.github.io.git quarto-$commit_hash

                        curl -s -H "Authorization: token ${GITHUB_TOKEN}" -X POST -d '{"title": "Updating submodule quarto to $commit_hash", "base":"master", "body":"Updating submodule quarto to $commit_hash"}' "https://api.github.com/repos/stan-dev/stan-dev.github.io/pulls"
                    """
                }
            }
        }

    }
    post {
        success { script { utils.mailBuildResults("SUCCESSFUL") } }
        unstable { script { utils.mailBuildResults("UNSTABLE", "stan-buildbot@googlegroups.com") } }
        failure { script { utils.mailBuildResults("FAILURE", "stan-buildbot@googlegroups.com") } }
    }
}