from otodom.otodom import Otodom


with Otodom() as bot:

    bot.land_first_page()
    bot.accept_cookies()
    bot.choose_city()
    bot.choose_max_min_price()
    bot.show_results()
    bot.get_and_save_all_links()

    bot.visit_all_links_and_save_parameters()
    
    print('Exiting...')
