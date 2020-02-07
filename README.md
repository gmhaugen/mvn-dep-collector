# mvn-dep-collector
Collects pom-dependencies based on a library filename.

1. Use mvnrep_cli.py to collect dependency-XML from https://mvnrepository.com/. Input is a file with libraries (ex. log4j-core-2.4.jar) separated by newline. The dependencies are collected in "dependencies.xml".
2. Copy the dependencies from "dependencies.xml" and paste into "pom.xml" within the <dependencies>-tag.
3. Run maven-dependency-check: mvn test org.owasp:dependency-check-maven:check
    Be aware that the first run takes a while.
4. See output for the different dependencies.

