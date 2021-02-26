import webbrowser


def main():
    for i in range(1,10):
        print(i)
        webbrowser.open_new_tab("http://localhost:8000/metrics")

main()