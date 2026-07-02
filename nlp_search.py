def detect_mood(query):

    query=query.lower()

    if any(word in query for word in [
        "party",
        "dance",
        "club",
        "celebration"
    ]):
        return "Party"
    

    elif any(word in query for word in [
        "happy",
        "fun",
        "cheerful",
        "good mood"
    ]):
        return "Happy"
    
    
    elif any(word in query for word in[
        "relax",
        "calm",
        "sleep",
        "study",
        "peaceful"
    ]):
        return "Relax"
    
    return None

