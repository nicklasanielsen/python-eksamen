class crime_identifier:
    def identify(crime=""):
        crime = crime.upper()

        if "UHELD" in crime:
            return "uheld"
        elif "VOLD" in crime:
            return "vold"
        elif "TYVERI" or "STJÅLET" in crime:
            return "tyveri"
        elif "BRAND" in crime:
            return "brand"
        elif "HÆRVÆRK" in crime:
            return "hærværk"
        elif "STOFFER" or "NARKO" or "EUFORISERENDE" in crime:
            "euforiserende stoffer"

        return "andre"
