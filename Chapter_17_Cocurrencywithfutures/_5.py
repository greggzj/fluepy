
'''

The Executor.map function is easy to use but it has a feature that may or may not be
helpful, depending on your needs: it returns the results exactly in the same order as the
calls are started: if the first call takes 10s to produce a result, and the others take 1s each,
your code will block for 10s as it tries to retrieve the first result of the generator returned
by map. After that, you’ll get the remaining results without blocking because they will
be done. That’s OK when you must have all the results before proceeding, but often it’s
preferable to get the results as they are ready, regardless of the order they were submitted.
To do that, you need a combination of the Executor.submit method and the fu
tures.as_completed function, as we saw in Example 17-4. We’ll come back to this
technique in “Using futures.as_completed” on page 527.

The combination of executor.submit and futures.as_comple
ted is more flexible than executor.map because you can submit
different callables and arguments, while executor.map is designed
to run the same callable on the different arguments. In
addition, the set of futures you pass to futures.as_completed may
come from more than one executor—perhaps some were created
by a ThreadPoolExecutor instance while others are from a Proc
essPoolExecutor.


Downloads with Progress Display and Error Handling
As mentioned, the scripts in “Example: Web Downloads in Three Styles” on page 505
have no error handling to make them easier to read and to contrast the structure of the
three approaches: sequential, threaded, and asynchronous.
In order to test the handling of a variety of error conditions, I created the flags2
examples:

flags2_common.py
    This module contains common functions and settings used by all flags2 examples,
    including a main function, which takes care of command-line parsing, timing, and
    reporting results. This is really support code, not directly relevant to the subject of
    this chapter, so the source code is in Appendix A, Example A-10.
flags2_sequential.py
    A sequential HTTP client with proper error handling and progress bar display. Its
    download_one function is also used by flags2_threadpool.py.
flags2_threadpool.py
    Concurrent HTTP client based on futures.ThreadPoolExecutor to demonstrate
    error handling and integration of the progress bar.
flags2_asyncio.py
    Same functionality as previous example but implemented with asyncio and
    aiohttp. This will be covered in “Enhancing the asyncio downloader Script” on
    page 554, in Chapter 18.


Be Careful When Testing Concurrent Clients
    When testing concurrent HTTP clients on public HTTP servers,
    you may generate many requests per second, and that’s how denialof-
    service (DoS) attacks are made. We don’t want to attack anyone,
    just learn how to build high-performance clients. Carefully
    throttle your clients when hitting public servers. For highconcurrency
    experiments, set up a local HTTP server for testing.
    Instructions for doing it are in the README.rst file in the 17-
    futures/countries/ directory of the Fluent Python code repository.


The most visible feature of the flags2 examples is that they have an animated, textmode
progress bar implemented with the TQDM package. I posted a 108s video on
YouTube to show the progress bar and contrast the speed of the three flags2 scripts.
In the video, I start with the sequential download, but I interrupt it after 32s because it
was going to take more than 5 minutes to hit on 676 URLs and get 194 flags; I then run
the threaded and asyncio scripts three times each, and every time they complete the
job in 6s or less (i.e., more than 60 times faster). Figure 17-1 shows two screenshots:
during and after running flags2_threadpool.py.

'''