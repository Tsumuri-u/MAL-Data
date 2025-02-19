import argparse
import scraper
import plotter

def main():
    anime_data = "mal_anime_data_fixed.csv"
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    scrape_parser = subparsers.add_parser("scrape")
    scrape_parser.add_argument("target", choices=["anime", "manga"])
    plot_parser = subparsers.add_parser("plot")
    plot_parser.add_argument("target", choices=["test", "scoretime", "scoreisekai", "histogramisekaimembers", "histogramisekaiscore"])
    
    args = parser.parse_args()
    
    if args.command == "scrape":
        if args.target == "anime":
            scraper.scrape_anime(62000)
        elif args.target == "manga":
            scraper.scrape_manga(180000)
    elif args.command == "plot":
        if args.target == "test":
            plotter.test(anime_data)
        elif args.target == "scoretime":
            plotter.score_over_time(anime_data)
        elif args.target == "scoreisekai":
            plotter.score_members_isekai(anime_data)
        elif args.target == "histogramisekaimembers":
            plotter.isekai_members_double_gaussian(anime_data)
        elif args.target == "histogramisekaiscore":
            plotter.isekai_score_double_gaussian(anime_data)
        

if __name__ == "__main__":
    main()