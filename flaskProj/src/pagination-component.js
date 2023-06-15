import React from 'react';

const Population = ({name, endpoint, cacheReqs}) => {
    const [elements, setElements] = React.useState([]);
    const [mappedElements, setMappedElements] = React.useState([]);
    const [exception, setError] = React.useState(null);

    async function fetchAndSet(cachedReq, moniker) {
        try 
        {
            const response = await fetch(endpoint + "/" + cachedReq + ".html");
            const data = await response.json();
            setElements((currentCache) => [...currentCache, data]);

            return (<object key={moniker + "-" + index.toString()} data={item}/>);
        }
        catch(err) 
        {
            setError(err);
        };
    };
    
    React.useEffect(() => {
        const mapElements = elements.map((item, moniker, index) =>
        (
            <object key={moniker + "-" + index.toString()} data={item}/>
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