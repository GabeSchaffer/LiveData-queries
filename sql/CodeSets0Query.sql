
SELECT
	*
FROM (
	SELECT XMLElement("CodeSet",
		XMLAttributes(DEFINITION AS "definition",
			CODE_SET AS "codeSetId",
			REPLACE(DESCRIPTION, UNISTR('\0000'), '') AS "description",
			DISPLAY AS "display"),
		
		(SELECT XMLAgg(XMLElement("CodeValue",
			XMLAttributes(REPLACE(DEFINITION, UNISTR('\0000'), '') AS "definition",
				REPLACE(DESCRIPTION, UNISTR('\0000'), '') AS "description",
				NULLIF(COLLATION_SEQ, 0) AS "sortKey",
				REPLACE(CDF_MEANING, UNISTR('\0000'), '') AS "meaning",
				CODE_VALUE AS "codeValueId",
				REPLACE(DISPLAY, UNISTR('\0000'), '') AS "display",
				ACTIVE_IND AS "isActive"))
		ORDER BY CODE_VALUE)
		FROM (CODE_VALUE) CODE_VALUE
		WHERE CODE_VALUE.CODE_SET = CODE_VALUE_SET.CODE_SET)).GetClobVal()
	FROM (CODE_VALUE_SET) CODE_VALUE_SET
	WHERE CODE_SET IN ({codeSets})
	ORDER BY CODE_SET)