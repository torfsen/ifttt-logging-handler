# A logging handler that forwards log messages to IFTTT.com.

[IFTTT.com][ifttt] is a platform that allows you to setup automatic reactions
to a wide range of events. This Python module provides a logging handler that
forwards log messages to IFTTT so that you can automatically react to them (for
example to get an e-mail if that cron job on some remote server you keep
forgetting about logs an error).

[ifttt]: https://ifttt.com


## Installation

    pip install -e git+https://github.com/torfsen/ifttt-logging-handler#egg=ifttt-logging-handler


## Usage

To use the handler, first visit https://ifttt.com/maker to make sure that you
have activated the "Maker" channel in your IFTTT account. That page also
displays your secret key which you will need later on to setup the logging
handler.

Once you've enabled the "Maker" channel, create a new IFTTT recipe using the
"Maker" channel's "Receive a web request" trigger. You will need to choose an
event name for the trigger (for example ``my-log-event``). As with any other
IFTTT recipe you can then select the action to be performed when the event is
triggered -- typically you want to be notified via email or SMS, but you're
free to choose any of the actions offered by IFTTT.

Using the handler from your Python code is easy:

    import logging
    from ifft_logging_handler import IFTTTLoggingHandler

    # Setup
    logger = logging.getLogger('my_logger')
    handler = IFTTTLoggingHandler(key='your-secret-ifttt-key',
                                  event='your-ifttt-event-name')
    logger.addHandler(handler)

    # Log things as usual
    logger.error('Oh noes, foobarizing the flux capacitor failed!')

Remember that you can set a level threshold on both the logger and the handler:
only log messages whose level is high enough will be forwarded to IFTTT.


## Using data from the log message in your IFTTT action

An IFTTT "Maker" event can receive up to three custom string values. By
default, these are the formatted log message, the location where the message
was logged (filename and line number), and, if available, the traceback
embedded in the log message.

The values can then be used in your IFTTT action using the placeholders (called
"ingredients" by IFTTT) `{{Value1}}`, `{{Value2}}`, and `{{Value3}}`.

You can customize which values are passed to IFTTT by passing a callback via
the `values` argument. The callback receives a `logging.LogRecord` instance and
can return up to 3 values:

    def my_values(record):
        return record.msg, some_important_value

    handler = IFTTTLoggingHandler('my-key', 'my-event', values=my_values)

