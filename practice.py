grades={"Math":85, "Physics":92}

score=grades.update({"Chemistry":78}).get("Chemistry")

print(score)