## COMPLETELY UNFINISHED AND UNTESTED
## BASICALLY JUST DON'T USE THIS

import pymongo


def query(db, text, state, city, tags, orderBy, page):
    PER_PAGE = 25
    results = []
    queryDict = {}
    if text != "":
        queryDict["$text"] = {"$search": text}
    if state != "":
        queryDict["location.state"] = state
    if city != "":
        queryDict["location.city"] = city
    if tags != []:
        queryDict["tags"] = {"$all": tags}
    if orderBy != "":
        for job in db.find(queryDict).sort(orderBy, -1).skip((page - 1) * PER_PAGE).limit(PER_PAGE):
            results.append(job)
    return results


if __name__ == "__main__":
    client = pymongo.MongoClient('localhost', 27017)
    db = client.jobDB
    jobs = db.jobs

    results = query(jobs, "Software Engineer", "MA", "Boston", ["python", "sql"], "numTags", 1)
    for item in results:
        print(item, end="\n\n")

    client.close()
