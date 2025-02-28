
SELECT
	*
FROM (
	SELECT XMLElement("Service",
		XMLAttributes(REPLACE(PRSNL_GROUP_DESC, UNISTR('\0000'), '') AS "description",
			PRSNL_GROUP_TYPE_CD AS "prsnl_group_type_cd",
			REPLACE(PRSNL_GROUP_NAME, UNISTR('\0000'), '') AS "name",
			ACTIVE_IND AS "isActive",
			PRSNL_GROUP_ID AS "prsnlGroupId"),
		
		(SELECT XMLAgg(XMLElement("P",
			XMLAttributes(PERSON_ID AS "id"))
		ORDER BY PERSON_ID)
		FROM (PRSNL_GROUP_RELTN) MEMBER
		WHERE MEMBER.PRSNL_GROUP_ID = SERVICE.PRSNL_GROUP_ID)).GetClobVal()
	FROM (PRSNL_GROUP) SERVICE
	WHERE PRSNL_GROUP_CLASS_CD = {personnelGroupClass}
	ORDER BY PRSNL_GROUP_ID)