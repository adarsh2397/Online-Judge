import platform,re, os, shutil, signal, sys, time, urllib, subprocess, codecs
from .models import Problems, Subs_code, Runs

timeoffset = 0
# Initialize Database and judge Constants
sql_hostname = '127.0.0.1'
sql_hostport = 3306
sql_username = 'aurora'
sql_password = 'aurora'
sql_database = 'aurora_main'
HOST, PORT = "127.0.0.1", 8723
# timeoffset = 19800

# Initialize Language Constants
php_prefix = "<?php ini_set('log_errors',1); ini_set('error_log','environ/error.txt'); ?>";
ioeredirect = " 0<environ/input.txt 1>environ/output.txt 2>environ/error.txt"

# Addition of new Language requires change below
# NOTE : You may need to add few lines in 'create' function too on addtion of new language.
langarr = {
    "AWK": {"extension": "awk", "system": "find /usr/bin/ -name awk", "execute": "awk -f environ/[exename].awk[inputfile]"},
    "Bash": {"extension": "sh", "system": "find /bin/ -name bash", "execute": "bash environ/[exename].sh[inputfile]"},
    "Brain": {"extension": "b", "system": "find /usr/bin/ -name bf", "execute": "bf environ/[exename].b[inputfile]"},
    "C": {"extension": "c", "system": "find /usr/bin/ -name cc",
          "compile": "cc environ/[codefilename].c -O2 -fomit-frame-pointer -o environ/[codefilename] -lm" + ioeredirect,
          "execute": "environ/[exename][inputfile]"},
    "C++": {"extension": "cpp", "system": "find /usr/bin/ -name g++",
            "compile": "g++ environ/[codefilename].cpp -O2 -fomit-frame-pointer -o environ/[codefilename]" + ioeredirect,
            "execute": "environ/[exename][inputfile]"},
    "C#": {"extension": "cs", "system": "find /usr/bin/ -name gmcs",
           "compile": "gmcs environ/[codefilename].cs -out:environ/[codefilename].exe" + ioeredirect,
           "execute": "mono environ/[exename].exe[inputfile]"},
    "Java": {"extension": "java", "system": "find /usr/bin/ -name javac",
             "compile": "javac -g:none -Xlint -d environ environ/[codefilename].java" + ioeredirect,
             "execute": "java -client -classpath environ [exename][inputfile]"},
    "JavaScript": {"extension": "js", "system": "find /usr/bin/ -name rhino",
                   "execute": "rhino -f environ/[exename].js[inputfile]"},
    "Pascal": {"extension": "pas", "system": "find /usr/bin/ -name fpc",
               "compile": "fpc environ/[codefilename].pas -O2 -oenviron/[codefilename]" + ioeredirect,
               "execute": "environ/[exename][inputfile]"},
    "Perl": {"extension": "pl", "system": "find /usr/bin/ -name perl", "execute": "perl environ/[exename].pl[inputfile]"},
    "PHP": {"extension": "php", "system": "find /usr/bin/ -name php", "execute": "php -f environ/[exename].php[inputfile]"},
    "Python": {"extension": "py", "system": "find /usr/bin/ -name python2",
               "execute": "python2 environ/[exename].py[inputfile]"},
    "Python3": {"extension": "py", "system": "find /usr/bin/ -name python3",
                "execute": "python3 environ/[exename].py[inputfile]"},
    "Ruby": {"extension": "rb", "system": "find /usr/bin/ -name ruby", "execute": "ruby environ/[exename].rb[inputfile]"},
    "Text": {"extension": "txt"}
}

# Define useful variables

running = 0
mypid = int(os.getpid())
timediff = 0
languages = []


# File Read/Write Functions
def file_read(filename):
    if not os.path.exists(filename): return "";
    f = codecs.open(filename, "r", "utf-8");
    d = f.read();
    f.close();
    return d.replace("\r", "")


def file_write(filename, data):
    f = codecs.open(filename, "w", "utf-8");
    f.write(data.replace("\r", ""));
    f.close();


# Systems Check
def system():
    global languages
    if not os.path.isdir("environ"): os.mkdir("environ");
    for lang in langarr:
        if (lang != "Text" and os.popen(langarr[lang]["system"]).read() != ""): languages.append(lang);


# Program Compilation
def create(codefilename, language):
    if (language not in ('C', 'C++', 'C#', 'Java', 'Pascal')): return
    print("Compiling Code File ...")
    result = None
    compilecmd = langarr[language]["compile"]
    compilecmd = compilecmd.replace("[codefilename]", codefilename)
    print(compilecmd)
    if language == "Java":
        os.system(compilecmd)
        if ((not os.path.exists("environ/" + codefilename + ".class")) and (
        not os.path.exists("environ/main/" + codefilename + ".class"))):
            result = "CE"
    elif language == "C#":
        os.system(compilecmd)
        if not os.path.exists("environ/" + codefilename + ".exe"):
            result = "CE"
    else:
        os.system(compilecmd)
        if not os.path.exists("environ/" + codefilename):
            result = "CE"

    if result == None:
        print("Code File Compiled to Executable.")
    else:
        print("Compilation Error")
    return result


# Program Execution
def execute(exename, language, timelimit):
    global running, timediff
    inputfile = " <environ/input.txt 1>environ/output.txt 2>environ/error.txt"
    if language == "Java" and not (os.path.exists("environ/" + exename + ".class")):
        exename = "main/" + exename
    cmd = '' + langarr[language]["execute"] + "; exit;"
    cmd = cmd.replace("[exename]", exename)
    cmd = cmd.replace("[inputfile]", inputfile)
    print(cmd)

    # os.system("chmod 100 .")
    if (os.path.exists("environ/input.txt")): os.system("chmod 777 environ/input.txt")
    if (os.path.exists("environ/error.txt")): os.system("chmod 777 environ/error.txt")
    if (os.path.exists("environ/output.txt")): os.system("chmod 777 environ/output.txt")

    starttime = time.time()
    proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
    t = 1
    time.sleep(timelimit)
    if proc.poll() is None:
        proc.kill()
        print("Timed out")
    t = proc.returncode
    endtime = time.time()
    timediff = endtime - starttime

    # os.system("chmod 750 .")
    os.system("pkill -u judge")
    print("Return Code : " + str(t))
    return t

def system_checks():
    # Perform system checks
    if (platform.system() != 'Linux'):
        print("Error : This script can only be run on Linux.")
        sys.exit(0);

    # Print Heading
    os.system("clear")
    print("\nArgus Online Judge : Execution Protocol\n");

    # Obtain lock
    if (os.path.exists("lock.txt")):
        print("Error : Could not obtain lock on Execution Protocol\n")
        print(
            "This problem usually occurs if you are trying to run two instances of this script on the same machine at the same time. However, if this is not the case, the solution to this problem would be to shut down all instances of this script, manually delete the 'lock.txt' file (which shall be in the same directory as this) and restart a single instance of it. The latter is usually due to an improper termination the last time this was run, or an error in the script itself.\n");
        sys.exit(1);
    else:
        lock = open("lock.txt", "w");
        print("Obtained lock on Execution Protocol\n");

    # System Check
    system()
    if len(languages) == 0:
        print("Error : No Languages supported on this System.")
        sys.exit(1);
    else:
        languages.append('Text');
    print("Supported Languages : " + str(languages) + "\n")
    sys.stdout.flush();


def runjudge(subId):
    system()
    # Connect to Database
    print(subId)
    print("Connecting to Server ...")
    print("Connected to Server ...")
    print()
    try:
        sub = Subs_code.objects.get(pk=subId)
    except (KeyError, Subs_code.DoesNotExist):
        print("The object is not present\n")
        return


    # Select an Unjudged Submission
    print("Selected Run ID %d for Evaluation." % (sub.run.id));

    os.system("rm -r environ/*");
    print("Cleared environironment for Program Execution.");

    # Initialize Variables
    result = None;
    timetaken = 0;
    running = 0
    sys.stdout.flush();
    # Write Code & Input File
    if result == None:
        if sub.run.language == "Java":
            codefilename = sub.run.name
        elif sub.run.language == "Text":
            codefilename = "output"
        else:
            codefilename = "code";
        codefile = codecs.open("environ/" + codefilename + "." + langarr[sub.run.language]["extension"], "w", "utf-8")
        if (sub.run.language == "PHP"): codefile.write(php_prefix);  # append prefix for PHP
        codefile.write(sub.code.replace("\r", ""));
        codefile.close();
        if "-cache" not in sys.argv:
            file_write("environ/input.txt", sub.run.problem.input);
        else:
            try:
                with open("io_cache/Aurora Online Judge - Problem ID " + str(sub.run.problem.id) + " - Input.txt"):
                    pass
            except IOError:
                file_write("io_cache/Aurora Online Judge - Problem ID " + str(sub.run.problem.id) + " - Input.txt",
                           sub.run.problem.input)
                file_write("io_cache/Aurora Online Judge - Problem ID " + str(sub.run.problem.id) + " - Output.txt",
                           sub.run.problem.output)
            shutil.copyfile("io_cache/Aurora Online Judge - Problem ID " + str(sub.run.problem.id) + " - Input.txt",
                            "environ/input.txt")
        print("Code & Input File Created.")

    # Compile, if required
    if result == None:
        result = create(codefilename, sub.run.language);  # Compile
    sys.stdout.flush();
    timelimit = float(sub.run.problem.timelimit)
    # Increase Time Limit in case some languages
    if sub.run.language in ('Java', 'Python', 'Python3', 'Ruby', 'PHP', 'C#', 'JavaScript'):
        if sub.run.language in ("Java", "C#", "JavaScript"):
            timelimit *= 2;
        elif sub.run.language in ("Python", "Ruby", "PHP", "Python3"):
            timelimit *= 3;

    # Run the program through a new thread, and kill it after some time
    if result == None and sub.run.language != "Text":
        running = 0
        print("Spawning process ...")
        t = execute(codefilename, sub.run.language, timelimit)
        # while running==0: pass # Wait till process begins
        print("Process Complete!")
        if t == 124:
            result = "TLE"
            timetaken = float(sub.run.problem.timelimit)
            # kill(codefilename,sub.run["language"])
            file_write('environ/error.txt', "Time Limit Exceeded - Process killed.")
        elif t == 139:
            file_write('environ/error.txt', 'SIGSEGV||Segmentation fault (core dumped)\n' + file_read("environ/error.txt"))
            timetaken = timediff
        elif t == 136:
            file_write('environ/error.txt', 'SIGFPE||Floating point exception\n' + file_read("environ/error.txt"))
            timetaken = timediff
        elif t == 134:
            file_write('environ/error.txt', 'SIGABRT||Aborted\n' + file_read("environ/error.txt"))
            timetaken = timediff
        elif t != 0:
            file_write('environ/error.txt', 'NZEC||return code : ' + str(t) + "\n" + file_read("environ/error.txt"))
            timetaken = timediff
        else:
            timetaken = timediff
    sys.stdout.flush();
    # Compare the output
    output = ""
    if result == None and sub.run.language != "Text" and file_read("environ/error.txt") != "":
        output = file_read("environ/output.txt")
        result = "RTE"
    if result == None:
        output = file_read("environ/output.txt")
        if "-cache" in sys.argv:
            sub.run.problem.output = file_read(
                "io_cache/Aurora Online Judge - Problem ID " + str(sub.run.id) + " - Output.txt")
        correct = sub.run.problem.output.replace("\r", "")
        if sub.run.problem.output is None: sub.run.problem.output = ""
        if output.endswith('\n'):
                output = output[:-1]
        if (output == correct):
            result = "AC"
        elif "S" in sub.run.problem.output and re.sub(" +", " ",
                                             re.sub("\n *", "\n", re.sub(" *\n", "\n", output))) == re.sub(" +",
                                                                                                           " ",
                                                                                                           re.sub(
                                                                                                               "\n *",
                                                                                                               "\n",
                                                                                                               re.sub(
                                                                                                                   " *\n",
                                                                                                                   "\n",
                                                                                                                   correct))):
            result = "AC"
        elif (re.sub(r"\s", "", output) == re.sub(r"\s", "", correct)):
            result = "AC" if "P" in sub.run.problem.output else "PE"
        else:
            result = "WA"
    print("Output Judgement Complete.")
    sub.run.result = result
    sub.run.time = timetaken
    if result == "AC":
        sub.run.problem.solved += 1
        sub.run.score = sub.run.problem.score
        count_runs = Runs.objects.all().filter(user=sub.run.user, score=sub.run.problem.score)
        if len(count_runs) == 0:
            print("YES")
            sub.run.user.userdetails.total_score += sub.run.score
            sub.run.user.userdetails.save()
        else: print(len(count_runs))

    # Write results to database
    error = file_read("environ/error.txt")
    sub.error = re.escape(error)
    sub.output = output
    sub.run.save()
    sub.save()
    sub.run.problem.total += 1
    # update the solved variable

    sub.run.problem.save()
    print("Result (%s,%.3f) updated on Server.\n" % (result, timetaken))
    sys.stdout.flush();
    # Commit changes

    print("Disconnected from Server.\n")
    sys.stdout.flush();