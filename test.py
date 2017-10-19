if __name__ == '__main__':
    # f = open('/home/cachecloud/Downloads/error.log', 'wa')
    import time, datetime, logging
    logging.basicConfig(
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        level=logging.WARNING,
        filename='/home/lpj/Downloads/error.log',
        filemode='w'
    )
    count = 1
    while 1:
        count += 1
        w_str = "this is mysql logging testing---" + str(count)
        logging.warning(w_str)

        time.sleep(5)