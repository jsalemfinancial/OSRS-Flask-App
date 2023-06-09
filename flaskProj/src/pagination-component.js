import React from 'react';

const Population = ({name, endpoint}) => {
    const [elements, setElements] = React.useState("");
    const [mappedElements, setMappedElements] = React.useState([]);
    const [exception, setError] = React.useState(null);

    React.useEffect(() => 
    {
        const fetcher = async () => 
        {
            try 
            {
                const response = await fetch(endpoint);
                const data = await response.json();
                setElements(Object.values(data).join(""));
            }
            catch(err) 
            {
                setError(err);
            };
        };

        fetcher();
    }, []);
    
    React.useEffect(() => {
        const mapElements = elements.split(',').map((htmlString, index) =>
        (
            <div key={"Chart-" + index.toString()} dangerouslySetInnerHTML={{__html: htmlString}}/>
        ));

        setMappedElements(mapElements);
    }, [elements]);
    /*
        Can't JSONify bytes. :,(
    */
    // const decodeCache = (data) => 
    // {
    //     let decodedData = [];

    //     for (const [key, value] of Object.entries(data)) {
    //         const buf = new ArrayBuffer(value.length, "base64");
    //         const decodedBuf = new TextDecoder().decode(buf);
    //         decodedData.push(decodedBuf.toString());
    //     }

    //     return decodedData;
    // };

    // console.log(exception);

    return (
        <>
          <h1>{name}</h1>
          <div className="populated-components-container">{mappedElements}</div>
        </>
      );
}

export default Population;