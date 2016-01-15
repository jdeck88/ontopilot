<http://rs.tdwg.org/dwc/terms/locality>
        a       <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> ;
        <http://www.w3.org/2000/01/rdf-schema#isDefinedBy>
                <http://rs.tdwg.org/dwc/terms/locality> .

<http://rs.tdwg.org/dwc/terms/occurrenceID>
        a       <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> , <http://www.w3.org/2000/01/rdf-schema#Class> ;
        <http://www.w3.org/2000/01/rdf-schema#isDefinedBy>
                <http://rs.tdwg.org/dwc/terms/occurrenceID> .

<obi:is_specified_output_of>
        a       <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> .

<obi:has_specified_output>
        a       <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> .

<http://rs.tdwg.org/dwc/terms/eventDate>
        a       <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> ;
        <http://www.w3.org/2000/01/rdf-schema#isDefinedBy>
                <http://rs.tdwg.org/dwc/terms/eventDate> .

<http://rs.tdwg.org/dwc/terms/Longitude>
        a       <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> ;
        <http://www.w3.org/2000/01/rdf-schema#isDefinedBy>
                <http://rs.tdwg.org/dwc/terms/Longitude> .

<http://rs.tdwg.org/dwc/terms/Latitude>
        a       <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> ;
        <http://www.w3.org/2000/01/rdf-schema#isDefinedBy>
                <http://rs.tdwg.org/dwc/terms/Latitude> .

<urn:phenophase_description>
        a       <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> ;
        <http://www.w3.org/2000/01/rdf-schema#isDefinedBy>
                <urn:phenophase_description> .

<file:///opt/jetty/temp/jetty-0.0.0.0-80-biocode-fims.war-_biocode-fims-any-8462970736449351377.dir/webapp/tripleOutput/phenophase_id>
        a       <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> ;
        <http://www.w3.org/2000/01/rdf-schema#isDefinedBy>
                <file:///opt/jetty/temp/jetty-0.0.0.0-80-biocode-fims.war-_biocode-fims-any-8462970736449351377.dir/webapp/tripleOutput/phenophase_id> .

<ark:/21547/vo2e08de556abf375552ba80333f6b04cb3>
        a                           <bco:observation_process> ;
        <http://rs.tdwg.org/dwc/terms/Latitude>
                "39.098499" ;
        <http://rs.tdwg.org/dwc/terms/Longitude>
                "-104.834297" ;
        <http://rs.tdwg.org/dwc/terms/eventDate>
                "2015-03-27T00:00:00.000-05:00" ;
        <http://rs.tdwg.org/dwc/terms/locality>
                "PPN_9050005" ;
        <obi:has_specified_output>  <ark:/21547/vn25336407> .

<ark:/21547/vn25336407>
        a       <http://rs.tdwg.org/dwc/terms/occurrenceID> ;
        <http://rs.tdwg.org/dwc/terms/occurrenceID>
                "5336407" .

<ark:/21547/vp2500>  a                <ppo:plant_phenological_stage> ;
        <file:///opt/jetty/temp/jetty-0.0.0.0-80-biocode-fims.war-_biocode-fims-any-8462970736449351377.dir/webapp/tripleOutput/phenophase_id>
                "500" ;
        <obi:is_specified_output_of>  <ark:/21547/vn25336407> ;
        <urn:phenophase_description>  "Flowers or flower buds" .

<ppo:plant_phenological_stage>
        a       <http://www.w3.org/2000/01/rdf-schema#Class> .

<bco:observation_process>
        a       <http://www.w3.org/2000/01/rdf-schema#Class> .
