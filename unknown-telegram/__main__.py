# -*- coding: utf-8 -*-
# Coded by @altfoxie with power of Senko!

if __package__ != "unknown-telegram":
    print("You need to run this as a module, not a script.")
else:
    if __name__ == "__main__":
        import asyncio

        from . import main

        loop = asyncio.get_event_loop()

        def exception_handler(_loop, _context):
            """Python sucks"""
            _loop.stop()
            if isinstance(_context["exception"], SystemExit):
                return
            raise _context["exception"]

        loop.set_exception_handler(exception_handler)
        loop.create_task(main.main())
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
